# -*- coding: utf-8 -*
from i8d.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter

from z3c.relationfield.relation import RelationValue
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone import api
from pyallpay import AllPay
from DateTime import DateTime
import random
import transaction

import logging


class ReturnUrl(BrowserView):
    """ Return URL
    """

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        itemInCart = request.cookies.get('itemInCart', '')
        itemInCart_list = itemInCart.split()

        with api.env.adopt_user(username="admin"):
            if not request.form['MerchantTradeNo']:
                return
            try:
                order = catalog({'Type':'Order', 'Title':request.form['MerchantTradeNo']})[0].getObject()
            except:
                return

            if not order.result:
                order.result = {}

            for key in request.form.keys():
                order.result[key] = request.form[key]

            transaction.commit()
            return


class ClientBackUrl(BrowserView):
    """ Client back url
    """

    template = ViewPageTemplateFile("template/client_back_url.pt")
    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        portal = api.portal.get()
#        itemInCart = request.cookies.get('itemInCart', '')
#        itemInCart_list = itemInCart.split()

        response.setCookie('itemInCart', '')
#        response.redirect('/logistics_map?MerchantTradeNo=%s' % request.form['MerchantTradeNo'])

        self.order = catalog({'Type':'Order', 'id':request.form['MerchantTradeNo']})[0]
        self.products = catalog({'Type':'Product', 'UID':self.order.productUIDs.keys()})
        if request.form.get('LogisticsType') == 'cvs':
            response.redirect('%s/logistics_map?MerchantTradeNo=%s&LogisticsType=%s&LogisticsSubType=%s' %
                (portal.absolute_url(), request.form.get('MerchantTradeNo'), request.form.get('LogisticsType'), request.form.get('LogisticsSubType'))
            )
            return

        # 計算佣金(聯盟行銷, 預設10%)
        self.orderTotal = self.order.getObject().amount
        if self.orderTotal:
            self.revenue = int(self.orderTotal * 0.10)
        else:
            self.revenue = 0

        self.traceCode = " \
            VA.remoteLoad({ \
                whiteLabel: { id: 8, siteId: 1193, domain: 'vbtrax.com' }, \
                conversion: true, \
                conversionData: { \
                    step: 'sale', \
                    revenue: '%s', \
                    orderTotal: '%s', \
                    order: '%s', \
                }, \
                locale: 'en-US', mkt: true \
            }); \
        " % (self.revenue, self.orderTotal, self.order.id)

        return self.template()


class CheckoutConfirm(BrowserView):
    """ Checkout Confirm
    """

    logger = logging.getLogger('bill.Checkout')
    template = ViewPageTemplateFile("template/checkout_confirm.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        portal = api.portal.get()

        if api.user.is_anonymous():
            self.profile = None
#            response.redirect('/')
#            return
        else:
            currentId = api.user.get_current().getId()
            self.profile = portal['members'][currentId]

        self.itemInCart = request.cookies.get('itemInCart', '')
        self.itemInCart_list = self.itemInCart.split()
        self.brain = catalog({'UID':self.itemInCart_list})

        self.shippingFee = 0
        self.discount = 0
        self.totalAmount = 0
        for item in self.brain:
            qty = int(request.cookies.get(item.UID, 1))
            self.totalAmount += item.salePrice * qty
            self.shippingFee += item.standardShippingCost
            self.discount += int(item.salePrice * item.maxUsedBonus) * int(request.cookies.get(item.UID, 1))

        if self.profile and self.discount > self.profile.bonus:
            self.discount = self.profile.bonus

# 應付金額：totalAmount + shippingFee - specailDiscount(滿3000折520)
        self.payable = self.totalAmount
#        if self.payable > 3000:
#            self.payable -= 520
        self.payable += self.shippingFee


        return self.template()


class Checkout(BrowserView):
    """ Checkout
    """

    logger = logging.getLogger('bill.Checkout')
    template = ViewPageTemplateFile("template/checkout.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        itemInCart = request.cookies.get('itemInCart', '')
        itemInCart_list = itemInCart.split()

        portal = api.portal.get()


        if request.form.get('LogisticsType') == 'home' and not request.form.get('address'):
            api.portal.show_message(message=_(u'Please fill full address information'), request=request, type='error')
            response.redirect('%s/@@checkout_confirm' % portal.absolute_url())
            return

        if api.user.is_anonymous():
            profile = None
        else:
            currentId = api.user.get_current().getId()
            profile = portal['members'][currentId]

        brain = catalog({'UID':itemInCart_list})
        totalAmount = 0
        itemName = ''
        itemDescription = ''
        productUIDs = {}
        shippingFee = 0
        discount = 0
        # specialDiscount , 滿3000折520
        specialDiscount = 0

        for item in brain:
            qty = int(request.cookies.get(item.UID, 1))
            productUIDs[item.UID] = qty
            totalAmount += item.salePrice * qty
            itemName += '%s $%s X %s#' % (item.Title, item.salePrice, qty)
            itemDescription += '%s: $%s X %s || ' % (item.Title, item.salePrice, qty)

            shippingFee += item.standardShippingCost
            if not api.user.is_anonymous():
                discount += int(item.salePrice * item.maxUsedBonus) * int(request.cookies.get(item.UID, 1))

        # 計算是否滿3000，是就折520 / 本活動已於8/24結束
#        if totalAmount >= 3000:
#            specialDiscount = 520

        # 8/25 開始促銷 start
        if totalAmount >= 5000:
            itemName += ', 滿5000加贈皇家珍珠鈣(100顆)'
            itemDescription += ', 滿3000加贈皇家珍珠鈣(100顆)'
        elif totalAmount >= 3000:
            itemName += ', 滿3000加贈皇家珍珠鈣(50顆)'
            itemDescription += ', 滿3000加贈皇家珍珠鈣(50顆)'
        # 8/25 開始促銷 end


        totalAmount += shippingFee

        if profile:
            if request.form['usingbonus'] == 'n':
                discount = 0
            if discount > profile.bonus:
                discount = profile.bonus
            totalAmount -= discount

            # 折抵 Special Discount
            totalAmount -= specialDiscount

            itemName += 'shipping Fee: %s, discount: %s' % (shippingFee, discount)
            itemDescription += 'shipping Fee: %s, discount: %s' % (shippingFee, discount)


            # Special Discount資訊
            if specialDiscount > 0:
                itemName += ', Special Discount: %s' % (specialDiscount)
                itemDescription += ', Special Discount: %s' % (specialDiscount)
        else:
            itemName += 'shipping Fee: %s' % (shippingFee)
            itemDescription += 'shipping Fee: %s' % (shippingFee)


            # 折抵 Special Discount
            totalAmount -= specialDiscount
            # Special Discount資訊
            if specialDiscount > 0:
                itemName += ', Special Discount: %s' % (specialDiscount)
                itemDescription += ', Special Discount: %s' % (specialDiscount)



        merchantTradeNo = '%s%s' % (DateTime().strftime('%Y%m%d%H%M%S'), random.randint(10000,99999))

        portal = api.portal.get()
        with api.env.adopt_roles(['Manager']):
#            import pdb ;pdb.set_trace()
            order = api.content.create(
                type='Order',
                title=merchantTradeNo,
                description = '%s, Total: $%s' % (itemDescription, totalAmount),
                productUIDs = productUIDs,
                amount = totalAmount,
                receiver = request.form.get('receiver', ''),
                phone = request.form.get('phone', ''),
                cellPhone = request.form.get('cellphone', ''),
                email = request.form.get('email',''),
                addr_city = request.form.get('city', ''),
                addr_district = request.form.get('district', ''),
                addr_zip = request.form.get('zipcode', ''),
                addr_address = request.form.get('address', ''),
                taxId = request.form.get('taxid', ''),
                companyTitle = request.form.get('companytitle', ''),
                container=portal['resource']['order'],
            )

            if profile:
                profile.bonus -= discount
            else:
                api.content.transition(obj=order, transition='publish')

            transaction.commit()

        paymentInfoURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.paymentInfoURL')
        clientBackURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.clientBackURL')
        payment_info = {'TotalAmount': totalAmount,
                        'ChoosePayment': 'ALL',
                        'MerchantTradeNo': merchantTradeNo,
                        'ItemName': itemName,
                        'PaymentInfoURL': paymentInfoURL,
                        'ClientBackURL': '%s?MerchantTradeNo=%s&LogisticsType=%s&LogisticsSubType=%s' %
                            (clientBackURL, merchantTradeNo, request.form.get('LogisticsType', 'cvs'), request.form.get('LogisticsSubType', 'UNIMART')),  #可以使用 get 帶參數
        }
        ap = AllPay(payment_info)
        # check out, this will return a dictionary containing checkValue...etc.
        dict_url = ap.check_out()
        # generate the submit form html.
        form_html = ap.gen_check_out_form(dict_url)

        return form_html

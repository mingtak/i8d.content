# -*- coding: utf-8 -* 
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
#        itemInCart = request.cookies.get('itemInCart', '')
#        itemInCart_list = itemInCart.split()

        response.setCookie('itemInCart', '')
#        response.redirect('/logistics_map?MerchantTradeNo=%s' % request.form['MerchantTradeNo'])

        self.order = catalog({'Type':'Order', 'id':request.form['MerchantTradeNo']})[0]
        self.products = catalog({'Type':'Product', 'UID':self.order.productUIDs.keys()})
        return self.template()


class CheckoutComfirm(BrowserView):
    """ Checkout
    """

    logger = logging.getLogger('bill.Checkout')
    template = ViewPageTemplateFile("template/checkout_comfirm.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        portal = api.portal.get()
        currentId = api.user.get_current().getId()
        self.profile = portal['members'][currentId]
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

        brain = catalog({'UID':itemInCart_list})
        totalAmount = 0
        itemName = ''
        itemDescription = ''
        productUIDs = {}
        for item in brain:
            qty = int(request.cookies.get(item.UID, 1))
            productUIDs[item.UID] = qty
            totalAmount += item.salePrice * qty
            itemName += '%s $%s X %s#' % (item.Title, item.salePrice, qty)
            itemDescription += '%s: $%s X %s || ' % (item.Title, item.salePrice, qty)

        merchantTradeNo = '%s%s' % (DateTime().strftime('%Y%m%d%H%M%S'), random.randint(10000,99999))

        portal = api.portal.get()
        with api.env.adopt_roles(['Manager']):
#            order =
            api.content.create(
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
#            order.productUIDs = []
#            for item in productUIDs:
#                order.productUIDs.append(item)
            transaction.commit()

        paymentInfoURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.paymentInfoURL')
        clientBackURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.clientBackURL')
        payment_info = {'TotalAmount': totalAmount,
                        'ChoosePayment': 'ALL',
                        'MerchantTradeNo': merchantTradeNo,
                        'ItemName': itemName,
                        'PaymentInfoURL': paymentInfoURL,
                        'ClientBackURL': '%s?MerchantTradeNo=%s' % (clientBackURL, merchantTradeNo),  #可以使用 get 帶參數
        }
        ap = AllPay(payment_info)
        # check out, this will return a dictionary containing checkValue...etc.
        dict_url = ap.check_out()
        # generate the submit form html.
        form_html = ap.gen_check_out_form(dict_url)

        return form_html

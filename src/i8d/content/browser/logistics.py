# -*- coding: utf-8 -* 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import random
import transaction
import urllib
import hashlib
from Products.CMFPlone.utils import safe_unicode
from pyallpay.utilities import do_str_replace
import logging


class LogisticsMap(BrowserView):
    """ Logistics map
    """
    logger = logging.getLogger('logistics.Logistics')
    template = ViewPageTemplateFile("template/logistics.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        logisticsMapURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsMapURL')
        merchantId = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.merchantID')
        serverReplyURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.serverReplyURL')

        self.actionURL = logisticsMapURL
        self.logistics_form = {
            'MerchantID': merchantId,
            'MerchantTradeNo': request.form['MerchantTradeNo'],
            'LogisticsType': 'CVS',
            'LogisticsSubType': 'FAMIC2C', # 待處理
            'IsCollection': 'Y', # 待處理
            'ServerReplyURL': serverReplyURL,
            'Device': 1, # 待處理
        }
        self.keys = self.logistics_form.keys()

        return self.template()


class LogisticsExpressCreate(BrowserView):
    """ Logistics Express Create
    """
    logger = logging.getLogger('logistics.LogisticsExpressCreate')
    template = ViewPageTemplateFile("template/logistics_express_create.pt")

    def encoded_dict(self, in_dict):
        out_dict = {}
        for k, v in in_dict.iteritems():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            out_dict[k] = v
        return out_dict


    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        portal = api.portal.get()

        hashKey = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsHashKey')
        hashIV = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsHashIV')
        order = portal['resource']['order'][request.form['merchantTradeNo']]

        logisticsExpressCreateURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsExpressCreateURL')
        merchantID = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.merchantID')
        merchantTradeNo = request.form['merchantTradeNo']
        merchantTradeDate = DateTime().strftime('%Y/%m/%d %H:%M:%S')
        logisticsType = 'CVS' # 待處理
        logisticsSubType = 'FAMI' # 待處理
        goodsAmount = order.result['TradeAmt']
        collectionAmount = order.result['TradeAmt'] # 待處理
        isCollection = 'Y' # 待處理
        goodsName = order.description[0:12]
        senderName = 'i8d.tw'
        senderPhone = '02-28973942'
        senderCellPhone = '0939-586835'
        receiverName = '王大明' # 待處理
        receiverPhone = '02-25586354' # 待處理
        receiverCellPhone = '0936-594874' # 待處理
        receiverEmail = 'andyfang51@gmail.com' # 待處理
        tradeDesc = order.description[0:100]
        serverReplyURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.serverReplyURL')
        clientReplyURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.clientReplyURL')
        logisticsC2CReplyURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsC2CReplyURL')
        receiverStoreID = order.logisticsMapResult['CVSStoreID']
        returnStoreID = order.logisticsMapResult['CVSStoreID'] # 不對？，應該是要北投這家店？

        self.formDict = {
            'MerchantId': merchantID,
            'MerchantTradeNo': merchantTradeNo,
            'MerchantTradeDate': merchantTradeDate,
            'LogisticsType': logisticsType,
            'LogisticsSubType': logisticsSubType,
            'GoodsAmount': goodsAmount,
            'CollectionAmount': collectionAmount,
            'IsCollection': isCollection,
            'GoodsName': goodsName,
            'SenderName': senderName,
            'SenderPhone': senderPhone,
            'SenderCellPhone': senderCellPhone,
            'ReceiverName': receiverName,
            'ReceiverPhone': receiverPhone,
            'ReceiverCellPhone': receiverCellPhone,
            'ReceiverEmail': receiverEmail,
            'TradeDesc': tradeDesc,
            'ServerReplyURL': serverReplyURL,
            'ClientReplyURL': clientReplyURL,
            'LogisticsC2CReplyURL': logisticsC2CReplyURL,
            'ReceiverStoreID': receiverStoreID,
            'ReturnStoreID': returnStoreID,
        }

        self.formDict = self.encoded_dict(self.formDict)
        sortedForm = sorted(self.formDict.iteritems())
        sortedForm.insert(0, ('HashKey', hashKey.encode('utf-8')))
        sortedForm.append(('HashIV', hashIV.encode('utf-8')))

        urlEncodeString = do_str_replace(urllib.quote(urllib.urlencode(sortedForm), '+%').lower())
        checkMacValue = hashlib.md5(urlEncodeString).hexdigest().upper()

        self.formDict['CheckMacValue'] = checkMacValue
        self.keys = self.formDict.keys()
        self.actionURL = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.logisticsExpressCreateURL')
        return self.template()


class LogisticsReply(BrowserView):
    """ Logistics Reply
    """
    logger = logging.getLogger('logistics.LogisticsReply')
#    template = ViewPageTemplateFile("template/client_back_url.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        brain = catalog({'Type': 'Order', 'id': request.form['MerchantTradeNo']})
        if not brain:
            return

        order = brain[0].getObject()
        if not order.logisticsMapResult:
            order.logisticsMapResult = {}

        for key in request.form.keys():
            order.logisticsMapResult[key] = request.form[key]

        transaction.commit()
        response.redirect('/logistics_express_create?merchantTradeNo=%s' % request.form['MerchantTradeNo'])
        return


class LogisticsClientReply(BrowserView):
    """ Logistics Client Reply, 訂單由系統向allpay發送建立，建立完成將information回傳到這裏
    """
    logger = logging.getLogger('logistics.LogisticsClientReply')
    template = ViewPageTemplateFile("template/logistics_client_reply.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        brain = catalog({'Type': 'Order', 'id': request.form['MerchantTradeNo']})
        if not brain:
            return

        order = brain[0].getObject()
        if not order.logisticsExpressResult:
            order.logisticsExpressResult = {}

        for key in request.form.keys():
            order.logisticsExpressResult[key] = request.form[key]

        transaction.commit()
        return self.template()


class LogisticsServerReply(BrowserView):
    """ Logistics Reply, Express Crate feedback，訂單完成後，若訂單狀態有更新，allpay會發送狀態到這裏
    """
    logger = logging.getLogger('logistics.LogisticsServerReply')

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog

        import pdb; pdb.set_trace()

        brain = catalog({'Type': 'Order', 'id': request.form['MerchantTradeNo']})
        if not brain:
            return

        order = brain[0].getObject()
        if not order.logisticsExpressResult:
            order.logisticsExpressResult = {}

        for key in request.form.keys():
            order.logisticsExpressResult[key] = request.form[key]

        transaction.commit()
#        response.redirect('/logistics_express_create?merchantTradeNo=%s' % request.form['MerchantTradeNo'])
        return

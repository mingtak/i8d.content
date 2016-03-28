from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
import logging
#from Acquisition import aq_inner
#from zope.component import getUtility
#from zope.intid.interfaces import IIntIds
#from zope.security import checkPermission
#from zc.relation.interfaces import ICatalog


class ShoppingCart(BrowserView):
    """ Shopping Cart
    """
    logger = logging.getLogger('REPORT')
    template = ViewPageTemplateFile("template/shopping_cart.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        logger = self.logger

        logger.info(self.request.cookies.items())
        logger.info(request.form)

        keys = request.form.keys()

        for key in keys:
            if catalog(UID=key):
                response.setCookie(key, request.form[key])
                response.redirect('/shopping_cart')
        return self.template()

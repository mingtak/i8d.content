from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
import logging


class CartAdd(BrowserView):
    """ Cart Add
    """

    logger = logging.getLogger('Add Item to Cart.')
    template = ViewPageTemplateFile("template/cart_state.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        logger = self.logger

        itemInCart = request.cookies.get('itemInCart', '')
        itemInCart_list = itemInCart.split()

        uid = request.form.get('uid', None)
        if not uid:
            return
        
        if request.form['uid'] not in itemInCart_list:
            itemInCart_list.append(request.form['uid'])
            itemInCart_list = list(set(itemInCart_list))
            itemInCart = ''
            for item in itemInCart_list:
                itemInCart += '%s ' % item
            request.response.setCookie('itemInCart', itemInCart)
            request.response.setCookie(uid, 1)
            self.itemInCart = itemInCart

        return self.template()




class CartDel(BrowserView):
    """ Cart Del
    """

    logger = logging.getLogger('Del Item to Cart.')
    template = ViewPageTemplateFile("template/cart_state.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        logger = self.logger

        itemInCart = request.cookies.get('itemInCart', '')
        itemInCart_list = itemInCart.split()

        uid = request.form.get('uid', None)

        if not uid:
            return

        if request.form['uid'] in itemInCart_list:
            try:
                itemInCart_list.remove(request.form['uid'])
            except:pass
            itemInCart = ''
            for item in itemInCart_list:
                itemInCart += '%s ' % item
            request.response.setCookie('itemInCart', itemInCart)
            self.itemInCart = itemInCart

        return self.template()



class CartUpdate(BrowserView):
    """ Shopping Cart
    """

    logger = logging.getLogger('Update Cart.')
    template = ViewPageTemplateFile("template/cart_state.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        logger = self.logger

        itemInCart = request.cookies.get('itemInCart', '')
        itemInCart_list = itemInCart.split()

        keys = request.form.keys()

        for key in keys:
            if catalog(UID=key):
                response.setCookie(key, request.form[key])
        response.redirect('/checkout_confirm')
        return


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


class MiniCartView(BrowserView):
    """ Mini Cart View
    """

    template = ViewPageTemplateFile("template/cart_state.pt")

    def __call__(self):
        request = self.request
        self.itemInCart = request.cookies.get('itemInCart', '')
        return template()

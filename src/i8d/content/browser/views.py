from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction
import csv


class ExportProducts(BrowserView):
    """ Export Products """

    index = ViewPageTemplateFile("template/export_products.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()

        com = request.form.get('com')

        if not com:
            response.redirect(portal.absolute_url())
            return

        if not portal['products'].has_key(com):
            response.redirect(portal.absolute_url())
            return

        comFolder = portal['products'][com]
        self.items = comFolder.getChildNodes()
        return self.index()


class CanSeeWithDateRange(BrowserView):
    """ Can See With Date Range """

    def __call__(self):
        context = self.context

        now = DateTime()
        effective = DateTime(context.EffectiveDate())
        expiration = DateTime() if context.ExpirationDate()=='None' else DateTime(context.ExpirationDate())
        if not api.user.is_anonymous() and set(api.user.get_roles()) & set(['Manager', 'Site Administrator']):
            return True
        if now >= effective and now <= expiration:
            return True
        else:
            return False


class ShippingMethodHomeAddress(BrowserView):
    """ Shipping Method Home Address
    """
    index = ViewPageTemplateFile("template/shipping_method_home_address.pt")

    def __call__(self):

        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()

        if api.user.is_anonymous():
            self.profile = None
        else:
            currentId = api.user.get_current().getId()
            self.profile = portal['members'][currentId]

        return self.index()


class ShippingMethod(BrowserView):
    """ Shipping Method
    """
    index = ViewPageTemplateFile("template/shipping_method.pt")

    def __call__(self):

        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()

        if api.user.is_anonymous():
            self.profile = None
        else:
            currentId = api.user.get_current().getId()
            self.profile = portal['members'][currentId]

        return self.index()


class InvoiceMethod(BrowserView):
    """ Invoice Method
    """


class WithoutPT(BrowserView):
    """ Without PT View
    """


class ProfileView(BrowserView):
    """ Profile View
    """


class OrderView(BrowserView):
    """ Order View
    """


class PostView(BrowserView):
    """ Post View
    """


class QuestionView(BrowserView):
    """ Question View
    """


class QuestionListView(BrowserView):
    """ Question List View
    """


class PostListView(BrowserView):
    """ Post List View
    """


class BrandView(BrowserView):
    """ Brand View (default)
    """


class ProductView(BrowserView):
    """ Product View (default)
    """


class CoverView(BrowserView):
    """ Cover View (default)
    """


class CanSeeBackend(BrowserView):
    """ Can See Backend
    """

    def __call__(self):

        request = self.request
        canSeeRoles = ['Manager', 'Site Administrator', 'Reader']

        if api.user.is_anonymous():
            return False
        else:
            roles = api.user.get_roles()
            for role in canSeeRoles:
                if role in roles:
                    return True
            if 'ishare/++add++Post' in request.getURL() or 'question/++add++Question' in request.getURL():
                return True
            return False


class I8dSitemap(BrowserView):
    """ i8d sitemap
    """


class I8dMacro(BrowserView):
    """ i8d macro
    """


class TestView(BrowserView):
    """ """

    def __call__(self):
        import pdb; pdb.set_trace()


class TestView2(BrowserView):

    index = ViewPageTemplateFile("template/testview2.pt")

    def __call__(self):
        context = self.context
        return self.index()


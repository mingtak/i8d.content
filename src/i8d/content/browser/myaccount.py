from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
import transaction
#from Acquisition import aq_inner
#from zope.component import getUtility
#from zope.intid.interfaces import IIntIds
#from zope.security import checkPermission
#from zc.relation.interfaces import ICatalog


class MyOrder(BrowserView):
    """ My Order
    """
    template = ViewPageTemplateFile("template/my_order.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        catalog = context.portal_catalog

        if api.user.is_anonymous():
            request.response.redirect('/')
            return

        self.currentUser = api.user.get_current()
        self.currentId = self.currentUser.getId()
        self.orders = catalog({'Creator':self.currentId, 'Type':'Order'},
                             sort_on='created', sort_order='reverse')

        try:
            self.myProfile = portal['members'][self.currentId]
        except:
            request.response.redirect('/')

        return self.template()


class AccountInfo(BrowserView):
    """ Account Information
    """
    template = ViewPageTemplateFile("template/account_info.pt")

    def update_info(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        catalog = context.portal_catalog
        myProfile = self.myProfile

        if request.form.get('name'):
            myProfile.title = request.form.get('name')
        myProfile.description = request.form.get('description')
        myProfile.cellPhone = request.form.get('cellphone')
        myProfile.phone = request.form.get('phone')
        myProfile.addr_city = request.form.get('city')
        myProfile.addr_district = request.form.get('district')
        myProfile.addr_zip = request.form.get('zipcode')
        myProfile.addr_address = request.form.get('address')
        myProfile.email = request.form.get('email')

        transaction.commit()
        return


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        catalog = context.portal_catalog

        if api.user.is_anonymous():
            request.response.redirect('/')
            return

        self.currentUser = api.user.get_current()
        self.currentId = self.currentUser.getId()

        try:
            self.myProfile = portal['members'][self.currentId]
        except:
            request.response.redirect('/')

        if request.method == 'POST' and request.form.get('currentid', '') == self.currentId:
            self.update_info()

        return self.template()


class MyAccount(BrowserView):
    """ My Account
    """
    template = ViewPageTemplateFile("template/my_account.pt")

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        catalog = context.portal_catalog

        if api.user.is_anonymous():
            request.response.redirect('/')
            return

        self.currentUser = api.user.get_current()
        self.currentId = self.currentUser.getId()
        self.orders = catalog({'Creator':self.currentId, 'Type':'Order'},
                             sort_on='created', sort_order='reverse')
        if self.orders:
            self.orders = self.orders[0:request.form.get('show', 5)]

        try:
            self.myProfile = portal['members'][self.currentId]
            self.ishareBrain = catalog({'Type':'Post', 'Creator': self.currentId})
            if self.ishareBrain:
                self.ishareBrain = self.ishareBrain[0:5]
            self.questionBrain = catalog({'Type':'Question', 'Creator': self.currentId})
            if self.questionBrain:
                self.questionBrain = self.questionBrain[0:5]
        except:
            request.response.redirect('/')

        return self.template()

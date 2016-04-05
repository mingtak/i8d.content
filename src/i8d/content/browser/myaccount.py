from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api

#from Acquisition import aq_inner
#from zope.component import getUtility
#from zope.intid.interfaces import IIntIds
#from zope.security import checkPermission
#from zc.relation.interfaces import ICatalog


class MyAccount(BrowserView):
    """ Profile View
    """
    template = ViewPageTemplateFile("template/my_account.pt")

    def __call__(self):
        context = self.context
        request = self.request
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
            self.myProfile = catalog({'Type':'Profile', 'id':self.currentId})[0]
        except:
            request.response.redirect('/')

        return self.template()

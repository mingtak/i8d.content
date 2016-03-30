from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api

#from Acquisition import aq_inner
#from zope.component import getUtility
#from zope.intid.interfaces import IIntIds
#from zope.security import checkPermission
#from zc.relation.interfaces import ICatalog


class ProfileView(BrowserView):
    """ Profile View
    """


class PostView(BrowserView):
    """ Post View
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

        canSeeRoles = ['Manager', 'Site Administrator']

        if api.user.is_anonymous():
            return False
        else:
            roles = api.user.get_roles()
            for role in canSeeRoles:
                if role in roles:
                    return True
            return False





class TestView(BrowserView):
    """ """


class TestView2(BrowserView):

    index = ViewPageTemplateFile("template/testview2.pt")

    def __call__(self):
        context = self.context
        return self.index()


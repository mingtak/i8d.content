from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api

#from Acquisition import aq_inner
#from zope.component import getUtility
#from zope.intid.interfaces import IIntIds
#from zope.security import checkPermission
#from zc.relation.interfaces import ICatalog


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


class TestView(BrowserView):
    """ """


class TestView2(BrowserView):

    index = ViewPageTemplateFile("template/testview2.pt")

    def __call__(self):
        context = self.context
        return self.index()


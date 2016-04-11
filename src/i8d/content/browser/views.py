from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction


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
        canSeeRoles = ['Manager', 'Site Administrator']

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





class TestView(BrowserView):
    """ """

    def __call__(self):
        import pdb; pdb.set_trace()


class TestView2(BrowserView):

    index = ViewPageTemplateFile("template/testview2.pt")

    def __call__(self):
        context = self.context
        return self.index()


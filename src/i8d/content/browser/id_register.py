from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction


class IdRegister(BrowserView):
    """ Id Register  """

    index = ViewPageTemplateFile("template/id_register.pt")

    def __call__(self):
        context = self.context
        return self.index()

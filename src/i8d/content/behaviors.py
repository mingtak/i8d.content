# -*- coding: utf-8 -*-
from i8d.content import _
from Products.CMFCore.interfaces import IDublinCore
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapts
from zope.interface import alsoProvides, implements
from zope.interface import provider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.field import NamedBlobImage, NamedBlobFile


class IBannerImage(model.Schema):
    """Add banner image to content
    """

    bannerImage = NamedBlobImage(
        title=_(u"Banner Image"),
        description=_(u"Banner image, about 1500X350 around."),
        required=True,
    )


alsoProvides(IBannerImage, IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class BannerImage(object):
    """
       Adapter for BannerImage
    """
    implements(IBannerImage)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    bannerImage = context_property("bannerImage")

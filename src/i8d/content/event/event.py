# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from plone import api


def moveContentToTop(item, event):
    """ Moves Item to the top of its folder """
    folder = item.getParentNode()
    if hasattr(folder, 'moveObjectsToTop'):
        folder.moveObjectsToTop(item.id)


def namedAnwserTitle(item, event):
    item.title = u'回覆：%s' % safe_unicode(item.getParentNode().Title())
    item.reindexObject()
    return


def testevent(item, event):
    """ """

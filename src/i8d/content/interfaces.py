# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from i8d.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class II8DContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IProduct(Interface):
    """ 產品 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class ICover(Interface):
    """ 首頁 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class IProfile(Interface):
    """ 個人頁面，含專家檔案 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class IForum(Interface):
    """ 專家給問 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class IProvider(Interface):
    """ 供應商檔案 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class IOrder(Interface):
    """ 訂單 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


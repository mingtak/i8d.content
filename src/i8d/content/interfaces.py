# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from i8d.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.formwidget.contenttree import ObjPathSourceBinder
from collective import dexteritytextindexer
#from zope.interface import invariant, Invalid
#from DateTime import DateTime
from datetime import datetime
class II8DContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


# 紅利點數發放比率，預設為1%(0.01)，基於防笨最高設定不得超過5%(0.05)
MIN_BONUS_RATE = 0.0
MAX_BONUS_RATE = 0.05
DEFAULT_BONUS_RATE = 0.01

# 使用紅利點數可折抵折扣率，以小數點表示百分比, 最小不打折，最多85折(15% off), 預設95折(5% off)
MIN_USED_BONUS_RATE = 0.0
MAX_USED_BONUS_RATE = 0.15
DEFAULT_USED_BONUS_RATE = 0.05


class IBrand(Interface):
    """ 品牌 """
    title = schema.TextLine(
        title=_(u"Brand Title"),
        required=True,
    )

    nickname = schema.Text(
        title=_(u"Brand Nickname"),
        description=_("Please listing all nickname that about this brand. For example, Microfost and MS, perline one record."),
        required=True,
    )

    image = NamedBlobImage(
        title=_(u"Brand Logo"),
        description=_(u"Brand logo image"),
        required=True,
    )


class IProduct(Interface):
    """ 產品 """
    title = schema.TextLine(
        title=_(u"Product Name"),
        required=True,
    )

    productId = schema.TextLine(
        title=_(u"Product Id"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    productUrl = schema.URI(
        title=_(u"Pruduct URL"),
        description=_(u"Product introduction web page include http:// or https://"),
        required=False,
    )

    inStock = schema.Bool(
        title=_(u"In Stock?"),
        description=_(u"If In Stock, Please check it."),
        default=True,
        required=False,
    )

    brand = schema.TextLine(
        title=_(u"Brand"),
        description=_(u"Brand name."),
        required=False,
    )

    """
    categoryTag = schema.TextLine(
        title=_(u"Category Tag"),
        description=_(u"Category tag for product, Provider define. Separated by commas."),
        required=False,
    )
    """

    listPrice = schema.Int(
        title=_(u"List Price"),
        description=_(u"The list price of the product."),
        required=True,
    )

    salePrice = schema.Int(
        title=_(u"Sale price"),
        description=_(u"Sale price for the product if different from the list price, must be <= listPrice."),
        required=True,
    )

    image_1 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image for header."),
        required=True,
    )

    image_2 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_4 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_5 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

 
    """    special = schema.TextLine(
        title=_(u"Special"),
        description=_(u"Used to denote a special offer. Can be used by a publisher to identify unique products, Will be YES, NO or empty."),
        required=False,
    ) """

    # 紅利點數發放比率，以小數點表示百分比
    bonusPoint = schema.Float(
        title=_(u"Bonus Point"),
        description=_(u"Bonus point setting, please filling decimal point. maximum is 0.05 (5%)"),
        default=DEFAULT_BONUS_RATE,
        min=MIN_BONUS_RATE,
        max=MAX_BONUS_RATE,
        required=True,
    )

    # 今日折扣，使用紅利點數可折抵折扣率，以小數點表示百分比
    maxUsedBonus = schema.Float(
        title=_(u"Maximum Used Bonus Points"),
        description=_(u"You can use a maximum bonus points."),
        default=DEFAULT_USED_BONUS_RATE,
        min=MIN_USED_BONUS_RATE,
        max=MAX_USED_BONUS_RATE,
        required=True,
    )

    dexteritytextindexer.searchable('promotionalText')
    promotionalText = RichText(
        title=_(u"Promotional Text"),
        description=_(u"Promotional Text, support html format richtext."),
        required=False,
    )

    # 產品要放在首頁推廣，則本欄必填, 該用 ReviewPortalContent? or ManagePortal? 再考量
    form.write_permission(heroText='cmf.ReviewPortalContent')
    heroText = schema.Text(
        title=_(u"Hero Text"),
        description=_(u"Promotional Text for Hero page"),
        required=False,
    )

    # 運費，以單品計算, 若一張訂單有多樣商品，須依規則另計
    standardShippingCost = schema.Int(
        title=_(u"Standard shipping cost"),
        description=_(u"Usually is the cost for the typical standard, lowest cost shipping method. This is provided for informational purposes and the actual shipping cost could vary depending on the visitor."),
        required=False,
    )

    lastUpdated = schema.Datetime(
        title=_(u"Last Updated"),
        description=_(u"Date of the most recent update to the product."),
        default=datetime.now(),
        required=True,
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

    heros = RelationList(
        title=_(u"Heros"),
        description=_(u"Rleated items for hero section"),
        value_type=RelationChoice(title=_(u"Related"),
                       vocabulary="plone.app.vocabularies.Catalog",),
        required=True,
    )

    newProduct = RelationList(
        title=_(u"New Product"),
        description=_(u"Rleated items for home page new product list"),
        value_type=RelationChoice(title=_(u"Related"),
                       vocabulary="plone.app.vocabularies.Catalog",),
        required=True,
    )

    hotProduct = RelationList(
        title=_(u"Hot Product"),
        description=_(u"Rleated items for home page not product list"),
        value_type=RelationChoice(title=_(u"Related"),
                       vocabulary="plone.app.vocabularies.Catalog",),
        required=True,
    )

    article = RelationList(
        title=_(u"Article"),
        description=_(u"Rleated items for home page article list"),
        value_type=RelationChoice(title=_(u"Related"),
                       vocabulary="plone.app.vocabularies.Catalog",),
        required=True,
    )

    question = RelationList(
        title=_(u"Question"),
        description=_(u"Rleated items for home page question list"),
        value_type=RelationChoice(title=_(u"Related"),
                       vocabulary="plone.app.vocabularies.Catalog",),
        required=True,
    )


class IProfile(Interface):
    """ 個人頁面，含專家檔案 """
    title = schema.TextLine(
        title=_(u"Profile Name"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


class IPost(Interface):
    """ 貼文分享 """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    form.write_permission(image='cmf.ReviewPortalContent')
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"If want to show this page to home page, please upload a image."),
        required=False,
    )

    form.write_permission(shortText='cmf.ReviewPortalContent')
    shortText = schema.TextLine(
        title=_(u"Short Text"),
        description=_(u"Short Text, show in Cover."),
        required=False,
    )

class IQuestion(Interface):
    """ 專家給問 """
    title = schema.TextLine(
        title=_(u"Question Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Question Detail"),
        required=True,
    )

    form.write_permission(image='cmf.ReviewPortalContent')
    image = NamedBlobImage(
        title=_(u"Image"),
        description=_(u"If want to show this page to home page, please upload a image."),
        required=False,
    )


class IAnswer(Interface):
    """ 回答(for 專家給問) """

    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )

    text = RichText(
        title=_(u"Reply Question"),
        required=True,
    )


class IProvider(Interface):
    """ 供應商檔案 """
    title = schema.TextLine(
        title=_(u"Provider Name"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    image = NamedBlobImage(
        title=_(u"Provider Logo"),
        description=_(u"Provider logo image"),
        required=False,
    )

    webSite = schema.URI(
        title=_(u"Website"),
        description=_(u"Provider website url, must include http:// or https://"),
        required=False,
    )

    form.write_permission(productsFile='cmf.ReviewPortalContent')
    productsFile = NamedBlobFile(
        title=_(u"Products File"),
        description=_(u"zip file, include a .cvs file and image files"),
        required=False,
    )


class IOrder(Interface):
    """ 訂單 """
    title = schema.TextLine(
        title=_(u"Order Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


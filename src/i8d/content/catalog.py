# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from i8d.content.interfaces import IBrand, IProduct, ICover, IProfile, IPost, IQuestion, IAnswer, IProvider, IOrder


@indexer(IProduct)
def hasImage1_indexer(obj):
    if obj.image_1:
        return True
    else:
        return False

@indexer(IOrder)
def productUIDs_indexer(obj):
    return obj.productUIDs

@indexer(IOrder)
def amount_indexer(obj):
    return obj.amount

@indexer(IProfile)
def orderState_indexer(obj):
    return obj.orderState

@indexer(IProfile)
def isExpert_indexer(obj):
    return obj.isExpert

@indexer(IProduct)
def productId_indexer(obj):
    # index 傳進 unicode 會有 error，改傳 utf-8 正確，此法暫解
    string = safe_unicode(obj.productId).encode('utf-8')
    return string


@indexer(IProduct)
def parentId_indexer(obj):
    return obj.getParentNode().id


@indexer(IProduct)
def lastUpdated_indexer(obj):
    return obj.lastUpdated


@indexer(IProduct)
def standardShippingCost_indexer(obj):
    return obj.standardShippingCost


@indexer(IProduct)
def maxUsedBonus_indexer(obj):
    return obj.maxUsedBonus


@indexer(IProduct)
def bonusPoint_indexer(obj):
    return obj.bonusPoint


@indexer(IProduct)
def salePrice_indexer(obj):
    return obj.salePrice


@indexer(IProduct)
def listPrice_indexer(obj):
    return obj.listPrice


"""
@indexer(IProduct)
def categoryTag_indexer(obj):
    result = []
    for item in obj.categoryTag.split(','):
        result.append(item.strip())
    return result
"""

@indexer(IProduct)
def productUrl_indexer(obj):
    return obj.productUrl


@indexer(IProduct)
def inStock_indexer(obj):
    return obj.inStock


@indexer(IProduct)
def brand_indexer(obj):
    # index 傳進 unicode 會有 error，改傳 utf-8 正確，此法暫解
    string = safe_unicode(obj.brand).encode('utf-8')
    return string


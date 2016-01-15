# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface

from i8d.content.interfaces import IBrand, IProduct, ICover, IProfile, IPost, IQuestion, IAnswer, IProvider, IOrder


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


@indexer(IProduct)
def categoryTag_indexer(obj):
    result = []
    for item in obj.categoryTag.split(','):
        result.append(item.strip())
    return result


@indexer(IProduct)
def productUrl_indexer(obj):
    return obj.productUrl


@indexer(IProduct)
def inStock_indexer(obj):
    return obj.inStock


@indexer(IProduct)
def brand_indexer(obj):
    return obj.brand

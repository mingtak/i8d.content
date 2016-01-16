# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from plone import api
import csv
import os


def importProducts(folder, event):
    """ Import Products """
    if not folder.productsFile:
        return
#    import pdb; pdb.set_trace()
    zipFolderName = '/tmp/%s' % folder.id
    zipFileName = '%s.zip' % folder.id
    with open('/tmp/%s' % zipFileName, 'w') as file:
        file.write(folder.productsFile.data)

    csvPath = '%s/%s' % (zipFolderName, zipFileName)
    with open(csvPath) as file:
        csvData = file.read()

    folder.productsFile = None
    folder.reindexObject()
    # 完成後記得刪檔刪資料夾

# -*- coding: utf-8 -*-
from i8d.content import _
from Products.CMFPlone.utils import safe_unicode
from plone import api
import csv
import zipfile
import transaction
import os
from plone import namedfile
from plone.app.textfield.value import RichTextValue
import logging

logger = logging.getLogger("i8d.content.event.importProducts")

def modifyItem():
def crateItem():

def importProducts(folder, event):
    """ Import Products """
    if not folder.productsFile:
        return
    if folder.productsFile.filename != '%s.zip' % folder.id:
        message = _(u"file name must be same as provider id and extension is zip.")
        api.portal.show_message(message=message, request=folder.REQUEST, type='error')
        folder.productsFile = None
        folder.reindexObject()
        return

    portal = api.portal.get()
    catalog = api.portal.get_tool(name='portal_catalog')

    zipFolderName = '/tmp/%s' % folder.id
    zipFileName = '%s.zip' % folder.id


    with open('/tmp/%s' % zipFileName, 'w') as file:
        file.write(folder.productsFile.data)

    with open('/tmp/%s' % zipFileName) as file:
        zf = zipfile.ZipFile(file)
        zf.extractall('/tmp')

#    import pdb; pdb.set_trace()
    csvPath = '%s/%s.csv' % (zipFolderName, folder.id)
    with open(csvPath, 'rb') as file:
        for row in csv.DictReader(file):
            if catalog({'Type':'Product', 'productId':row['productId'], 'path':folder.getPhysicalPath()}):
                continue
            else:
                try:
                    item = api.content.create(
                        type='Product',
                        title=row['title'],
                        productId=row['productId'],
                        description=row['description'],
                        productUrl=row['productUrl'],
                        inStock=True if row['inStock'].strip().lower() == 'y' else False,
                        brand=row['brand'],
                        listPrice=int(row['listPrice']),
                        salePrice=int(row['salePrice']),
                        standardShippingCost=int(row['standardShippingCost']),
                        container=portal['products'][folder.id],
                    )
                    item.setSubject(tuple(row['subjects'].split(',')))
                    with open('%s/%s' % (zipFolderName, safe_unicode(row['image_1'].strip()))) as file:
                        item.image_1 = namedfile.NamedBlobImage(data=file, filename=safe_unicode('%s' % file.name.split('/')[-1]))
                    try:
                        with open('%s/%s' % (zipFolderName, safe_unicode(row['image_2'].strip()))) as file:
                            item.image_2 = namedfile.NamedBlobImage(data=file, filename=safe_unicode('%s' % file.name.split('/')[-1]))
                    except:pass
                    try:
                        with open('%s/%s' % (zipFolderName, safe_unicode(row['image_3'].strip()))) as file:
                            item.image_3 = namedfile.NamedBlobImage(data=file, filename=safe_unicode('%s' % file.name.split('/')[-1]))
                    except:pass
                    item.promotionalText = RichTextValue(safe_unicode(row['promotionalText']))
                    item.reindexObject()
                    transaction.commit()
                except:
                    logger.error('%s: productId:%s, title:%s ' % (_(u"Import product error"), row['productId'], row['title']))
                    continue
    folder.productsFile = None
    folder.reindexObject()
    # 完成後記得刪檔刪資料夾

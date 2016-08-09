from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction
import csv
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from bs4 import BeautifulSoup
from Products.CMFPlone.utils import safe_unicode
from plone.app.textfield.value import RichTextValue
from plone import namedfile
import html2text
import urllib2


class ImportIshareNer(BrowserView):
    """ Import Ishare from National Education Radio """

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        catalog = context.portal_catalog
        htmlHandle = html2text.HTML2Text()
        htmlHandle.ignore_images = True

        url = "http://eradio.ner.gov.tw/rss/?_sp=news"

        doc = urllib2.urlopen(url)
        soup = BeautifulSoup(doc.read(), 'xml')

        for item in soup.find_all('item'):
            title = item.title.string
            if catalog(Title=title):
                continue
            text = item.description.string
            description = htmlHandle.handle(text)
            html = BeautifulSoup(item.description.string, 'lxml')
            try:
                imgUrl = html.img['src']
                imgRaw = urllib2.urlopen(imgUrl)
                img = imgRaw.read()
                imgFile = namedfile.NamedBlobImage(data=img, filename=u'image.png')
            except:
                img = None

            ishare = api.content.create(
                type='Post',
                container=portal['ishare'],
                title=safe_unicode(title),
                shortText='%s...' % description[0:20],
                text = RichTextValue(safe_unicode(text))
            )
            if img:
                ishare.image = imgFile
            api.content.transition(obj=ishare, transition='reject')
        return

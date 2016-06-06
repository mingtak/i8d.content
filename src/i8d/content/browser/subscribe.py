# -*- coding: utf-8 -*-
from i8d.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
import urllib, urllib2
import json
import transaction


class Subscribe(BrowserView):

    template = ViewPageTemplateFile("template/subscribe.pt")


    def post(self, url, data):
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()


    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        catalog = context.portal_catalog
        portal = api.portal.get()

        if not request.form.get('email'):
            response.redirect(portal.absolute_url())
            return
        if not request.form.get('g-recaptcha-response'):
            return self.template()

        secret = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.googleSecret')
        postUrl = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret':secret,
            'response':request.form.get('g-recaptcha-response'),
            'remoteip':request.get('REMOTE_ADDR'),
        }

        recaptchaResult = json.loads(self.post(postUrl, data))

        email = request.form.get('email')
        if not (recaptchaResult.get('success') and email):
            response.redirect(portal.absolute_url())
            return

        subscribe = portal['resource']['subscribe']

        if email not in subscribe.subscribeList:
            subscribe.subscribeList.append(email)
            transaction.commit()

        api.portal.show_message(message=_(u'You are already subscribe, thanks.'), request=request, type='info')
        response.redirect(portal.absolute_url())
        return

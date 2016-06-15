# -*- coding: utf-8 -*-
from i8d.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import urllib, urllib2
import json
import transaction


class AddNewUser(BrowserView):
    """ Add New User """

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
        portal = api.portal.get()

        recaptchaResponse, email, name = request.form.get('g-recaptcha-response'), request.form.get('email'), request.form.get('name')
        if recaptchaResponse and email and name:
            pass
        else:
            api.portal.show_message(message=_(u'Please fill every field !'), request=request)
            response.redirect(portal.absolute_url())
            return

        secret = api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.googleSecret')
        postUrl = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret':secret,
            'response':request.form.get('g-recaptcha-response'),
            'remoteip':request.get('REMOTE_ADDR'),
        }

        recaptchaResult = json.loads(self.post(postUrl, data))

        if not (recaptchaResult.get('success') and email):
            api.portal.show_message(message=_(u'Please fill every field !'), request=request)
            response.redirect(portal.absolute_url())
            return

#帳號重複要處理
        user = api.user.create(
            username='noob',
            email='noob@plone.org',
            password='secret',
        )

        import pdb; pdb.set_trace()

        return



class IdRegister(BrowserView):
    """ Id Register """

    index = ViewPageTemplateFile("template/id_register.pt")

    def __call__(self):
        return self.index()


class IdLogin(BrowserView):
    """ Id Login """

    index = ViewPageTemplateFile("template/id_login.pt")

    def __call__(self):
        return self.index()


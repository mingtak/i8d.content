# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from plone import api


def checkProfile(event):
    """ Check Profile for User Loggedin event """
    portal = api.portal.get()
    currentUser = api.user.get_current()
    currentId = currentUser.getId()
    if portal['members'].has_key(currentId):
        return
    else:
        with api.env.adopt_roles(['Manager']):
            api.content.create(
                type='Profile',
                id=currentId,
                title=currentUser.getProperty('fullname'),
                bonus=api.portal.get_registry_record('i8d.content.browser.coverSetting.ICoverSetting.initialBonus'),
                container=portal['members']
            )

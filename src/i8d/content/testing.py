# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import i8d.content


class I8DContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=i8d.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'i8d.content:default')


I8D_CONTENT_FIXTURE = I8DContentLayer()


I8D_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(I8D_CONTENT_FIXTURE,),
    name='I8DContentLayer:IntegrationTesting'
)


I8D_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(I8D_CONTENT_FIXTURE,),
    name='I8DContentLayer:FunctionalTesting'
)


I8D_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        I8D_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='I8DContentLayer:AcceptanceTesting'
)

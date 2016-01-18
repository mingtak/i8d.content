from i8d.content import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form
from zope import schema


class ICoverSetting(Form.Schema):
    serviceExplanation = schema.Text(
        title=_(u"Service Explanation"),
        description=_(u"Header service explanation"),
        required=False,
    )

    brandShowInNav = schema.Text(
        title=_(u"Brand Show In Nav"),
        description=_(u"help_show_in_nav"),
        required=False,
    )

    providerShowInNav = schema.Text(
        title=_(u"Provider Show In Nav"),
        description=_(u"help_show_in_nav"),
        required=False,
    )

    productShowInNav = schema.Text(
        title=_(u"Product Show In Nav"),
        description=_(u"help_show_in_nav"),
        required=False,
    )


class CoverSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ICoverSetting

CoverSettingControlPanelView = layout.wrap_form(CoverSettingControlPanelForm, ControlPanelFormWrapper)
CoverSettingControlPanelView.label = _(u"Cover Setting")

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


class CoverSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ICoverSetting

CoverSettingControlPanelView = layout.wrap_form(CoverSettingControlPanelForm, ControlPanelFormWrapper)
CoverSettingControlPanelView.label = _(u"Cover Setting")

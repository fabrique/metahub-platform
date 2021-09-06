from django import forms
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks
from wagtailstreamforms.fields import _fields, register, BaseField
from wagtailstreamforms.streamfield import FormFieldStreamBlock
from wagtailstreamforms.wagtailstreamforms_fields import DropdownField

from .utils import NonRecursiveFormFieldStreamBlock

parental_fields = 'single_field', 'multi_field', 'fieldset', 'form_row'

_fields.pop('datetime')
_fields.pop('url')
_fields.pop('date')
_fields.pop('multifile')
_fields.pop('hidden')
_fields.pop('dropdown')

@register('single_field')
class SingleFieldField(BaseField):
    """ Field that supports creation of a form consisting of a single field """
    form_fields = FormFieldStreamBlock([], max_num=1)
    icon = 'fa-plus'
    label = _('Single field')

    @classmethod
    def get_formfield_label(cls, block_value):
        return block_value['title']

    def get_form_block(self):
        return blocks.StructBlock([
            ('form_fields',
             NonRecursiveFormFieldStreamBlock(
                 exclude=[*parental_fields, 'birth_date'],
                 max_num=1,
             )),
        ], icon=self.icon, label=self.label)


@register('multi_field')
class MultiFieldField(BaseField):
    """ Field that supports creation of a form consisting of multiple fields """
    form_fields = FormFieldStreamBlock([])
    icon = 'fa-plus'
    label = _('Multiple fields')

    @classmethod
    def get_formfield_label(cls, block_value):
        return block_value['title']

    def get_form_block(self):
        return blocks.StructBlock([
            ('form_fields', NonRecursiveFormFieldStreamBlock(include=['fieldset'])),
        ], icon=self.icon, label=self.label)


@register('fieldset')
class FieldsetField(BaseField):
    form_fields = FormFieldStreamBlock([])
    icon = 'fa-plus'

    @classmethod
    def get_formfield_label(cls, block_value):
        return block_value['title']

    def get_form_block(self):
        return blocks.StructBlock([
            ('title', blocks.CharBlock(required=False)),
            ('form_fields', NonRecursiveFormFieldStreamBlock(include=[
                'form_row',
                ])),
        ], icon=self.icon, label=self.label)


@register('form_row')
class FormRowField(BaseField):
    form_fields = FormFieldStreamBlock([])
    icon = 'fa-plus'

    @classmethod
    def get_formfield_label(cls, block_value):
        return 'form row'

    def get_form_block(self):
        return blocks.StructBlock([
            ('form_fields',
             NonRecursiveFormFieldStreamBlock(exclude=[
                 *parental_fields,
                ])),
        ], icon=self.icon, label=self.label)


@register('birth_date')
class DateField(BaseField):
    field_class = forms.DateField
    widget = forms.SelectDateWidget(years=range(now().year - 17, now().year - 100, -1))
    icon = "date"
    label = _("Birth date")


# @register('tac_checkbox')
# class TermsAndConditionsCheckbox(BaseField):
#     field_class = forms.BooleanField
#     icon = "tick"
#     label = _("Terms and Conditions")
#
#     def get_form_block(self):
#         return blocks.StructBlock(
#             [
#                 ("help_text", blocks.CharBlock(required=False)),
#             ],
#             icon=self.icon,
#             label=self.label,
#         )
#
#     @classmethod
#     def get_formfield_label(cls, block_value):
#         return 'tac_checkbox'
#
#     @classmethod
#     def get_formfield_required(cls, block_value):
#         return True
#
#     def get_options(self, block_value):
#         return {
#             "label": 'stub',
#             "help_text": self.get_formfield_help_text(block_value),
#             "required": self.get_formfield_required(block_value),
#             "initial": False,
#         }


# @register('target_recipient')
# class TargetRecipientDropdown(BaseField):
#     field_class = forms.ChoiceField
#     icon = "mail"
#     label = _('Target recipient')
#
#     def get_form_block(self):
#         return blocks.StructBlock(
#             [
#                 ("label", blocks.CharBlock()),
#                 ("help_text", blocks.CharBlock(required=False)),
#                 ("required", blocks.BooleanBlock(required=False)),
#                 ("empty_label", blocks.CharBlock(required=False)),
#                 ("choices", blocks.ListBlock(blocks.StructBlock([
#                     ('label', blocks.CharBlock(label='label')),
#                     ('email', blocks.EmailBlock(label='email')),
#                 ], label="Option"))),
#             ],
#             icon=self.icon,
#             label=self.label,
#         )
#
#     def get_options(self, block_value):
#         options = super().get_options(block_value)
#         choices = [(c['email'].strip(), c['label'].strip())
#                    for c in block_value.get("choices")]
#         if block_value.get("empty_label"):
#             choices.insert(0, ("", block_value.get("empty_label")))
#         options.update({"choices": choices})
#         return options


# _fields.pop('dropdown')
# @register('dropdown')
# class NewDropdownField(DropdownField):
#     def get_options(self, block_value):
#         options = super().get_options(block_value)
#         if block_value.get("label"):
#             self.widget = forms.Select(attrs={'placeholder': block_value["label"]})
#         return options

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Site
from wagtailmodelchooser.edit_handlers import ModelChooserPanel
from wagtailstreamforms.models.form import AbstractForm, Form


from .blocks import MailToAction
from .utils import NonRecursiveFormFieldStreamBlock, get_fields_flat, \
    form_get_email_fields


def monkeypatch_method(cls):
    """
    from <somewhere> import <someclass>

    @monkeypatch_method(<someclass>)
    def <newmethod>(self, args):
        return <whatever>
    """
    def decorator(func):
        def bound(self, *args, **kwargs):
            return func.__get__(self, cls)(*args, **kwargs)
        setattr(cls, func.__name__, bound)
        return func
    return decorator

# It is currently hard to make a custom StreamForms Form model, so we extend and
# alter the default one instead.

""" Forms field creation starts with an option to create a fieldset """# MKR disabled sinlge field for now, refactor out multifield in between step later if needed
Form._meta.get_field('fields').stream_block =\
    NonRecursiveFormFieldStreamBlock(
        [],
        required=True,
        include=('multi_field'),
        # include=('single_field', 'multi_field'),
        max_num=1,
    )


# """ Forms can define a mail that is sent to the user """
# confirmation_mail = models.ForeignKey(
#     'mails.Mail', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Confirmation mail',
#     help_text='Define a mail that is sent to the form submitter.')
# Form.add_to_class('confirmation_mail', confirmation_mail)
# Form.edit_handler.children[0].children.append(ModelChooserPanel('confirmation_mail'))
# def clean_confirmation_mail(self):
#     if 'send_confirmation_mail' in self.process_form_submission_hooks:
#         if not self.confirmation_mail:
#             raise ValidationError(
#                 _('Please specify a confirmation mail object to mail to the form submitter or uncheck the send confirmation mail flag.'))
#         if not any(form_get_email_fields(self)):
#             raise ValidationError(_('Please add an e-mail type field to the form or make the confirmation mail option blank.'))

#
# """ Forms can define people to mail to """
Form.add_to_class('actions', StreamField(
    verbose_name=_('Actions'), blank=True, block_types=[
        ('mail_action', MailToAction()),
    ]
))
Form.edit_handler.children[0].children.append(StreamFieldPanel('actions'))
for child in list(Form.edit_handler.children[0].children):
    if isinstance(child, MultiFieldPanel) and child.children[0].field_name == 'success_message':
        Form.edit_handler.children[0].children.remove(child)
def clean_actions(self):
    if 'mail_form_submission_data' in self.process_form_submission_hooks:
        has_mail_to_action = any(action.block.name == 'mail_action' for action in self.actions)
        has_mail_to_field = any(field['type'] == 'target_recipient' for field in get_fields_flat(self))
        if not (has_mail_to_action or has_mail_to_field):
            raise ValidationError(
                _('Please specify a recipient to mail to when using'
                  ' the "mail form submission data" hook.'))

@monkeypatch_method(Form)
def clean(self):
    super(Form, self).clean()
    clean_actions(self)
    # clean_confirmation_mail(self)
# Ready for some hackiness to get the form type
@monkeypatch_method(Form.objects.__class__)
def single_field(self):
    """ Retrieve all form instances that only have a single form field """
    return self.filter(fields__contains='"type": "single_field"')
@monkeypatch_method(Form.objects.__class__)
def multi_field(self):
    """ Retrieve all form instances that only have a multiple fields """
    return self.filter(fields__contains='"type": "multi_field"')
# Set some defaults
Form._meta.get_field('process_form_submission_hooks').default = ['save_form_submission_data']
Form._meta.get_field('submit_button_text').default = 'Verzenden'
Form._meta.get_field('template_name').default = 'streamforms/form_block.html'


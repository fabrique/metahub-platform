import magic
import logging
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import Template, Context
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from wagtailstreamforms.hooks import register
from wagtailstreamforms.utils.general import get_slug_from_string

from metahub.mails.models import Mail
from metahub.streamforms.utils import get_fields_flat, form_get_email_fields, \
    get_variable_from_label


logger = logging.getLogger("metahub")

@register('construct_submission_form_fields')
def fields_from_fieldsets(form_fields):
    """ Flattens the field set structure, returning a list of the actual fields """
    form_type = form_fields[0]['type']
    if form_type == 'multi_field':
        form_fields = form_fields[0]['value']['form_fields']
        new_fields = []
        for field_set in form_fields:
            for item in field_set['value']['form_fields']:
                if 'form_fields' in item['value']:
                    new_fields.extend(item['value']['form_fields'])
                else:
                    new_fields.append(item)
        return new_fields
    elif form_type == 'single_field':
        return form_fields[0]['value']['form_fields']


@register('construct_submission_form_fields')
def fix_missing_labels(form_fields):
    for field in form_fields:
        if 'label' not in field['value']:
            field['value']['label'] = field['type']
    return form_fields

#MKR disabled for now

# @register('process_form_submission')
# def send_confirmation_mail(instance, form):
#     """ Send confirmation mail to submitter """
#     mail_obj: Mail = instance.confirmation_mail
#     submission_data = form.cleaned_data.copy()
#
#     data = {}
#     for field in get_fields_flat(instance):
#         if not field['value'].get('label'):
#             continue
#         label = field['value']['label']
#         slug = get_slug_from_string(label)
#         variable = get_variable_from_label(label)
#         value = submission_data.get(get_slug_from_string(label), '?')
#         if hasattr(form.fields[slug], 'choices'):
#             choices = dict(form.fields[slug].choices)
#             if isinstance(value, list):
#                 value = '\n' + '\n'.join(
#                     ' - ' + striptags(choices.get(subvalue)) for subvalue in value)
#             else:
#                 value = striptags(choices.get(value))
#         data[variable] = value
#
#     subject = Template(mail_obj.subject).render(Context(data))
#     message = Template(mail_obj.text).render(Context(data))
#
#     recipient_label = next(form_get_email_fields(instance))['value']['label']
#     recipient = data[get_variable_from_label(recipient_label)]
#
#     if hasattr(settings, 'WAGTAILADMIN_NOTIFICATION_FROM_EMAIL'):
#         from_email = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
#     elif hasattr(settings, 'DEFAULT_FROM_EMAIL'):
#         from_email = settings.DEFAULT_FROM_EMAIL
#     else:
#         from_email = 'webmaster@localhost'
#
#     connection = get_connection()
#     kwargs = {
#         'connection': connection,
#         'headers': {
#             'Auto-Submitted': 'auto-generated',
#         },
#     }
#     mail = EmailMultiAlternatives(subject, strip_tags(message), from_email, [recipient], **kwargs)
#     mail.attach_alternative(message, 'text/html')
#     mail.send()




@register('process_form_submission')
def mail_form_submission_data(instance, form):
    """ Mails the form submission data """

    # copy the cleaned_data so we dont mess with the original
    submission_data = form.cleaned_data.copy()

    # if hasattr(form.page, 'correspondence_name'):
    #     name = form.page.correspondence_name
    # else:
    #     name = form.page.title
    name = form.page.title

    logger.info('debugging mails here')

    lines = []
    recipients = []
    for field in get_fields_flat(instance):
        if not field['value'].get('label'):
            continue
        label = field['value']['label']
        slug = get_slug_from_string(label)
        value = submission_data[get_slug_from_string(label)]
        if field['type'] == 'target_recipient':
            choices = dict(form.fields[slug].choices)
            # revalidate email-address
            if value in choices:
                recipients.append(value)
        elif hasattr(form.fields[slug], 'choices'):
            choices = dict(form.fields[slug].choices)
            if isinstance(value, list):
                value = '\n' + '\n'.join(
                    ' - ' + striptags(choices.get(subvalue)) for subvalue in value)
            else:
                value = striptags(choices.get(value))

        lines.append('{}: {}'.format(label, value))

    from django.utils.safestring import mark_safe
    message = render_to_string('qm_streamforms/mails/mail.html', {
        'page_title': name,
        'form_data': mark_safe('<br/>\n'.join(lines)),
    })

    for action in instance.actions:
        if action.block.name == 'mail_action':
            recipients.append(action.value['email_address'])

    if not recipients:
        raise RuntimeError(
            f'No recipients specified to mail form data to for form {name} ({instance.pk})'
        )

    if hasattr(settings, 'WAGTAILADMIN_NOTIFICATION_FROM_EMAIL'):
        from_email = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
    elif hasattr(settings, 'DEFAULT_FROM_EMAIL'):
        from_email = settings.DEFAULT_FROM_EMAIL
    else:
        from_email = 'webmaster@localhost'

    connection = get_connection()
    kwargs = {
        'connection': connection,
        'headers': {
            'Auto-Submitted': 'auto-generated',
        },
    }
    subject = _('Form submission: %(name)s') % {'name': name}
    mail = EmailMultiAlternatives(subject, strip_tags(message), from_email, recipients, **kwargs)
    mail.attach_alternative(message, 'text/html')

    # attach any files submitted
    for field in form.files:
        for file in form.files.getlist(field):
            file.seek(0)
            mail.attach(file.name, file.read(), file.content_type)

    logger.info('mail from {} to {} sent'.format(from_email, recipients))

    return mail.send()



# from django.core.mail import EmailMessage
# from django.template.defaultfilters import pluralize
# from mailchimp3.mailchimpclient import MailChimpError
#
# from wagtailstreamforms.hooks import register
#
# from smartocto.core.utils import get_mailchimp_client
#
#
# @register('process_form_submission')
# def subscribe_to_mailchimp(instance, form):
#
#     list_id = instance.advanced_settings.mailchimp_list_id
#     email = ''
#     first_name = ''
#     last_name = ''
#     for field, value in form.cleaned_data.items():
#         value = str(value)  #dirty i know
#         if field.find('name') != -1:
#             if field.find('first') !=-1:
#                 first_name = value
#             if field.find('last') !=-1 or field.find('surname') !=-1:
#                 last_name = value
#         if value.find('@') != -1:
#             email = value
#
#     if email:
#
#         client = get_mailchimp_client()
#         try:
#             client.lists.members.create(list_id, {
#                 'email_address': email,
#                 'status': 'subscribed',
#                 'merge_fields': {
#                     'FNAME': first_name,
#                     'LNAME': last_name,
#                 },
#             })
#             print('Subscribed {} ({} {}) to mailchimp list {}'.format(email, first_name, last_name, list_id))
#         except MailChimpError as e:
#             status = e.args[0].get('status')
#             if status == 400:
#                 # Already subscribed
#                 pass
#             else:
#                 print('Failed to subscribe {}'.format(email))


# @register('process_form_submission')
# def email_submission(instance, form):
#     """ Send an email with the submission. """
#
#     addresses = [instance.advanced_settings.to_address]
#     if not addresses:
#         return None
#
#     content = ['Please see below submission\n', ]
#     from_address = 'website@smartocto.com'
#
#     subject = 'New Form Submission : %s' % instance.title
#
#     # build up the email content
#     for field, value in form.cleaned_data.items():
#         if field in form.files:
#             count = len(form.files.getlist(field))
#             value = '{} file{}'.format(count, pluralize(count))
#         elif isinstance(value, list):
#             value = ', '.join(value)
#         content.append('{}: {}'.format(field, value))
#     content = '\n'.join(content)
#
#     # create the email message
#     email = EmailMessage(
#         subject=subject,
#         body=content,
#         from_email=from_address,
#         to=addresses
#     )
#
#     # attach any files submitted
#     for field in form.files:
#         for file in form.files.getlist(field):
#             file.seek(0)
#             email.attach(file.name, file.read(), file.content_type)
#
#     # finally send the email
#     email.send()

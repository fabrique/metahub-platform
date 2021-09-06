import re

from django.template import Template, Context

from metahub.mails.models import Mail, PersonalizedMail


def get_mail(key):
    return Mail.objects.get(key=key)


def personalize(mail: Mail, interpretation):
    context = {k: getattr(interpretation, k) for k in dir(interpretation) if not k.startswith('_')}
    r = lambda s: Template(s).render(Context(context))
    return PersonalizedMail(subject=r(mail.subject), body=r(mail.text))

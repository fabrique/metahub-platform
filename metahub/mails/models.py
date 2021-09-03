from typing import NamedTuple

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtailmodelchooser import register_model_chooser

# from qatar_museums.mails.config import mails


@register_model_chooser
class Mail(models.Model):
    key = models.CharField(unique=True, max_length=255, editable=False)
    title = models.CharField('Internal title', max_length=255, blank=True)
    subject = models.CharField(max_length=255)
    text = models.TextField(help_text='Add variables with double accolades, like Hello, {{ first_name }}! Available variables depend on the form being sent.')

    panels = [
        FieldPanel('title'),
        FieldPanel('subject'),
        FieldPanel('text'),
    ]

    def save(self, **kwargs):
        if not self.key:
            prev = Mail.objects.order_by('-pk').first()
            self.key = f'mail-{prev.pk + 1 if prev else 1}'
        return super().save(**kwargs)

    def __str__(self):
        return self.title or f'{self.subject} ({self.pk})'


class PersonalizedMail(NamedTuple):
    subject: str
    body: str

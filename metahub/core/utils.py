import random

from django.db import models
from django.utils.formats import date_format
from django.utils.html import format_html
from wagtail.admin.edit_handlers import EditHandler
from django.utils.translation import ugettext_lazy as _


class ReadOnlyPanel(EditHandler):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )

    def render(self):
        value = getattr(self.instance, self.attr)
        if callable(value):
            value = value()
        return format_html('<div style="padding-top: 1.2em;">{}</div>', value)

    def render_as_object(self):
        return format_html(
            '<fieldset><legend>{}</legend>'
            '<ul class="fields"><li><div class="field">{}</div></li></ul>'
            '</fieldset>',
            self.heading, self.render())

    def render_as_field(self):
        return format_html(
            '<div class="field">'
            '<label>{}{}</label>'
            '<div class="field-content">{}</div>'
            '</div>',
            self.heading, (':'), self.render())


def format_date(date):
    if date:
        return date_format(date, 'd F Y')
    return ''


class MetaHubThemeColor(models.TextChoices):
    MAGENTA = 'theme--pink', _('Magenta pink')
    STRAWBERRY = 'theme--magenta', _('Strawberry red')
    SAPPHIRE = 'theme--blue', _('Sapphire blue')
    PHLOX = 'theme--purple', _('Royal purple')


def get_random_color():
    return random.choice([e for e in MetaHubThemeColor])










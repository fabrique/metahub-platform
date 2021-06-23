from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.utils.translation import ugettext_lazy as _

from .models import Author


@modeladmin_register
class PersonAdmin(ModelAdmin):
    list_display = 'pk', 'name'
    menu_icon = 'fa-users'
    menu_label = _("Authors")
    model = Author
    menu_order = 600
    search_fields = 'name'
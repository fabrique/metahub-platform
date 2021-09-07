from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from metahub.collection.models import BaseCollectionArtist, BaseCollectionObject


class SyncButtonHelper(ButtonHelper):
    def sync_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.edit_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            "url": reverse("synchronise"),
            "label": _("Synchronise Beecollect"),
            "classname": cn,
            "title": _("Synchronise Beecollect"),
        }


class BaseCollectionArtistAdmin(ModelAdmin):
    model = BaseCollectionArtist
    menu_label = "Artists"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("first_name", "last_name", "date_added")

modeladmin_register(BaseCollectionArtistAdmin)


class BaseCollectionObjectAdmin(ModelAdmin):
    model = BaseCollectionObject
    menu_label = "Objects"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "date_added")
    search_fields = ("title", "bc_inventory_number")
    button_helper_class = SyncButtonHelper

modeladmin_register(BaseCollectionObjectAdmin)

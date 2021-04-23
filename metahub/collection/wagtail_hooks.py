from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import CollectionCategory, BaseCollectionArtist, BaseCollectionObject


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

modeladmin_register(BaseCollectionObjectAdmin)
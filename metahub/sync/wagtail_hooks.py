from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from metahub.sync.models import BeeCollectSyncOccurrence


class ImportLogAdmin(ModelAdmin):
    model = BeeCollectSyncOccurrence
    menu_label = "Import logs"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("date_done", "date_data_dump", "success",
                    "objects_in_dump", "objects_added", "objects_changed", "objects_removed",
                    "artists_in_dump", "artists_added", "artists_changed", "artists_removed")

modeladmin_register(ImportLogAdmin)


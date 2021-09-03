from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin

from metahub.mails.models import Mail


@modeladmin_register
class MailAdmin(ModelAdmin):
    add_to_settings_menu = True
    list_display = '__str__', 'subject'
    model = Mail
    menu_icon = 'mail'

from django.template import Library
from starling.interfaces.atoms import AtomLinkRegular

from wagtail.core.models import Site

from metahub.menu.models import Menu
from metahub.starling_metahub.structures.interfaces import StructureMenuBarRegular, StructureMenuHeaderRegular

register = Library()

@register.simple_tag(takes_context=True)
def get_menu_header_component(context):

    request = context['request']
    site = request.site
    language = request.LANGUAGE_CODE

    menu = Menu.for_site_and_language(site, language)
    menu_pages = menu.menu_items.all()

    menu_items = [
        AtomLinkRegular(
            href= menuitem.page.url if menuitem.page else menuitem.custom_link_value,
            title=menuitem.link_title if menuitem.link_title else menuitem.page.title,
        ) for menuitem in menu_pages
    ]

    return StructureMenuHeaderRegular(
        menu_items=menu_items,
        logo_href=menu.get_root_url()
    )

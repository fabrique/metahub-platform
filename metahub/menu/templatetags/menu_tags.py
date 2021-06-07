# from django.template import Library
# from starling.interfaces.atoms import AtomLinkRegular
#
# from wagtail.core.models import Site
#
# from metahub.menu.models import Menu
# from metahub.starling_metahub.structures.interfaces import StructureMenuBarRegular
#
# register = Library()
#
# @register.simple_tag(takes_context=True)
# def get_menu_items(context):
#     request = context['request']
#     site = request.site
#
#     menu_pages = Menu.for_site(site).menu_items.all()
#
#     menu_items = [
#         AtomLinkRegular(
#             href= menuitem.page.url if menuitem.page else menuitem.custom_link_value,
#             title=menuitem.link_title if menuitem.link_title else menuitem.page.title,
#             icon_before=menuitem.icon_before, #'custom/ic_slash',
#             icon_after=menuitem.icon_after,
#         ) for menuitem in menu_pages
#     ]
#
#     #icon_before: 'custom/ic_slash', icon_after: 'custom/ic_search'
#
#     return StructureMenuBarRegular(
#         menu_items=menu_items,
#         logo_href=Site.objects.get(is_default_site=True).root_url
#     )
#

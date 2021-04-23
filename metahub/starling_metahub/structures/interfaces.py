from typing import NamedTuple, Iterable

from starling.interfaces.atoms import AtomLinkRegular


class StructureMenuBarRegular(NamedTuple):
    menu_items: Iterable[AtomLinkRegular] = ()
    menu_button_title: str = 'Menu'
    navigation_aria_label: str = 'navigation'
    logo_href: str = ''


class StructureFooterBarSimple(NamedTuple):
    context: bool = False #whether context ribbon is present on the page
    content_page: bool = False
    links: Iterable[AtomLinkRegular] = ()


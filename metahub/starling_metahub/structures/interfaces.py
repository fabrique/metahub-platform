from typing import NamedTuple, Iterable, Sequence

from starling.interfaces.atoms import AtomLinkRegular


class StructureMenuBarRegular(NamedTuple):
    menu_items: Iterable[AtomLinkRegular] = ()
    menu_button_title: str = 'Menu'
    navigation_aria_label: str = 'navigation'
    main_navigation_aria_label: str = 'main navigation'
    logo_href: str = ''
    languages: Sequence = []


class StructureFooterBarSimple(NamedTuple):
    year: str = ''
    footer_links: Iterable[AtomLinkRegular] = ()


class StructureMenuHeaderRegular(NamedTuple):
    menu_items: Iterable[AtomLinkRegular] = ()
    logo_href: str = ''
    languages: Sequence = []
    has_logo: bool = True



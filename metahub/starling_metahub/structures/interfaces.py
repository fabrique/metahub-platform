from typing import NamedTuple, Iterable, Sequence

from django.utils.translation import ugettext_lazy as _

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


class StructureCookieBarRegular(NamedTuple):
    text: str = _('This website uses cookies and similar techniques for an optimal visitor experience.')
    button_accept_title: str  = _('Accept')
    button_reject_title: str = _('Reject')
    button_save_title: str = _('Save')
    button_accept_all_title: str = _('Accept all')
    customize_title: str = _('Change settings')
    customize_text: str = _("By deactivating one or more categories it's possible that certain parts of the website won't function as intended. You can always change your settings at a later time.")
    link_information: dict = {'href': _('/en/cookies/'), 'title': _('More information')}
    categories: Sequence = [
        {'name': 'functional', 'title': _('Functional cookies'),
         'text' : _('These cookies are necessary for a functioning website. You cannot deactivate these cookies.')},
        {'name': 'embeds', 'title': _('Third party cookies'),
         'text': _('These third party cookies are necessary to play Vimeo or YouTube content within the website.')},
        {'name': 'analytics', 'title': _('Analytic cookies'),
         'text': _('These cookies are used to monitor website usage and improve website performance and user experience.')}]

from typing import NamedTuple, Optional, Union, Iterable

from starling.interfaces.atoms import AtomPictureRegular
from starling.typing import Picture

from ..typings import PictureAccessible


class AtomDropdownOption(NamedTuple):
    title: str = ''
    value: str = ''
    number: str = ''


class AtomDropdownFilterRegular(NamedTuple):
    id: str = ''
    classes: str = ''
    name: str = ''
    placeholder: str = ''
    error: str = ''
    options: Iterable[AtomDropdownOption] = ()
    required: bool = False
    disabled: bool = False
    type: str = 'select'


class AtomVideoEmbedRegular(NamedTuple):
    classes: str = ''
    video_id: str = ''
    video_type: str = 'youtube'
    href: str = '#'
    autoplay: bool = False
    button_play_title: str = 'Play'
    picture: AtomPictureRegular = AtomPictureRegular()


class AtomFigureAccessibleRegular(NamedTuple):
    picture: PictureAccessible = AtomPictureRegular()
    caption: str = ''
    classes: str = ''


class AtomPaginationButtonRegular(NamedTuple):
    title: str = ''
    href: str = ''
    current: bool = False
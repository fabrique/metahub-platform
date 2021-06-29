from typing import NamedTuple, Iterable

from starling.interfaces.atoms import AtomLinkRegular, AtomPictureRegular
from starling.typing import Picture
from wagtail.core.models import Page


class MoleculeObjectCardRegular(NamedTuple):
    href: str = ''
    title: str = ''
    name: str = ''
    type: str = ''
    variant: str = 'object'
    date: str = ''
    classes: str = ''
    picture: AtomPictureRegular = AtomPictureRegular()

class MoleculeLinkRegular(NamedTuple):
    title: str = ''
    href: str = ''

class MoleculeContextCardRegular(NamedTuple):
    href: str = ''
    title: str = ''
    type: str = ''
    classes: str = ''
    color: str = ''
    target: str = ''
    picture: AtomPictureRegular = AtomPictureRegular()


class MoleculeLinkListRegular(NamedTuple):
    classes: str = ''
    direction: str = 'vertical'
    title: str = ''
    links: Iterable[AtomLinkRegular] = ()


class MoleculeAudioPlayer(NamedTuple):
    title: str = ''
    file_title: str = ''
    file_subtitle: str = ''
    file: str = ''
    audio_transcript: str = ''


class MoleculeCollectionCategoryCardRegular(NamedTuple):
    title: str = ''
    subtitle: str = ''
    image: AtomPictureRegular = AtomPictureRegular()
    href: str = ''
    target: str = ''


class MoleculeCardRegular(NamedTuple):
    title: str = ''
    label: str = ''
    text: str = ''
    theme_color: str = ''
    picture: Picture = None
    href: str = ''
    target: str = ''
    classes: str = ''
    date: str = ''


class MoleculeExploreCardRegular(NamedTuple):
    title: str = ''
    label: str = ''
    text: str = ''
    theme_color: str = ''
    picture: Picture = None
    href: str = ''
    classes: str = ''
    type: str = ''
    subtitle: str = ''
from typing import NamedTuple, Iterable

from starling.interfaces.atoms import AtomPictureRegular as AtomPictureRegular, AtomFigureRegular, AtomLinkRegular

from ..atoms.interfaces import AtomVideoEmbedRegular
from ..molecules.interfaces import MoleculeObjectCardRegular, MoleculeAudioPlayer, MoleculeCollectionCategoryCardRegular


class OrganismSearchHeaderRegular(NamedTuple):
    id: str = ''
    title: str = ''
    subtitle: str = ''
    pictures: Iterable[AtomPictureRegular] = ()
    is_homepage: bool = False
    live_search_url: str = ''
    search_url: str = ''
    picture_index: int = 0
    variant: str = 'default'


class OrganismHeroHeaderMultiImageRegular(NamedTuple):
    id: str = ''
    information: dict = { 'title': '', 'name': '', 'date' : ''}
    theme: str = 'blue'
    expandable: bool = True
    pictures: Iterable[AtomPictureRegular] = ()
    context: bool = False
    height: str = ''


class OrganismHeroHeaderVideoRegular(NamedTuple):
    id: str = ''
    title: str = ''
    video: AtomVideoEmbedRegular = AtomVideoEmbedRegular()


class OrganismImageIntroRegular(NamedTuple):
    id: str = ''
    classes: str = ''
    description: dict = {'text': ''}
    information: dict = {'title': '', 'name': ''}
    reading_time: str = ''
    type: str = ''
    audio: MoleculeAudioPlayer = MoleculeAudioPlayer()
    pictures: Iterable[AtomPictureRegular] = ()
    minimal: bool = True
    expandable : bool = True
    favinfo: dict = {}


class OrganismVideoIntroRegular(NamedTuple):
    id: str = ''
    intro: str = ''
    reading_time: str = ''
    video: AtomVideoEmbedRegular = AtomVideoEmbedRegular()


class OrganismContentDoubleQuoteRichTextRegular(NamedTuple):
    id : str = ''
    text: str = ''
    quote: str = ''
    attribution: str = ''


class OrganismObjectMosaicChoiceRegular(NamedTuple):
    id: str = ''
    title: str = ''
    series_cards: Iterable[MoleculeObjectCardRegular] = ()


class OrganismLinkListRegular(NamedTuple):
    id: str = ''
    title: str = ''
    links: Iterable[AtomLinkRegular] = ()


class OrganismContentSingleAudioRegular(NamedTuple):
    id: str = ''
    audio_fragment: MoleculeAudioPlayer = MoleculeAudioPlayer()


class OrganismCollectionCategoriesRegular(NamedTuple):
    id: str = ''
    title: str = ''
    cards: Iterable[MoleculeCollectionCategoryCardRegular] = ()


class OrganismObjectHighlightsRegular(NamedTuple):
    """
    Not directly linked to its block, contents are deferred in page model.
    """
    id: str = ''
    title: str = ''
    introduction: str = ''
    cards: Iterable = ()
    all_highlights_url: str = '/'


class OrganismThemeHighlightsRegular(NamedTuple):
    """
    Not directly linked to its block, contents are deferred in page model.
    """
    id: str = ''
    title: str = ''
    subtitle: str = ''
    theme_categories: Iterable[str] = ()
    themes: Iterable = ()


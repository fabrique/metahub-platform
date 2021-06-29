from typing import NamedTuple, Iterable, Sequence

from starling.interfaces.atoms import AtomPictureRegular as AtomPictureRegular, AtomFigureRegular, AtomLinkRegular
from starling.interfaces.molecules import MoleculeCardRegular

from ..atoms.interfaces import AtomVideoEmbedRegular
from ..molecules.interfaces import MoleculeObjectCardRegular, MoleculeAudioPlayer, MoleculeCollectionCategoryCardRegular


class OrganismContentSingleRichTextRegular(NamedTuple):
    id: str = ''
    text: str = ''

    def get_context_container(self):
        return 'text'


class  OrganismContentSingleImageRegular(NamedTuple):
    id: str = ''
    figure: AtomFigureRegular = AtomFigureRegular()
    caption: str = ''


class OrganismContentSingleVideoRegular(NamedTuple):
    id: str = ''
    classes: str = ''
    video: AtomVideoEmbedRegular = AtomVideoEmbedRegular()
    caption: str = ''
    caption_number: str = ''


class OrganismContentDoubleImageRichTextRegular(NamedTuple):
    id : str = ''
    figure: AtomFigureRegular = AtomFigureRegular()
    text: str = ''
    link: AtomLinkRegular = AtomLinkRegular()

    def get_context_container(self):
        return 'text'


class OrganismRelatedItemsRegular(NamedTuple):
    """
    Detail page component
    """
    id: str = ''
    title: str = ''
    related_objects: Iterable[MoleculeObjectCardRegular] = ()


class OrganismHeroImageHeaderRegular(NamedTuple):
    """
    Content page component - just the image as header
    """
    id: str = ''
    align: str = 'fullbleed'
    picture: AtomPictureRegular = AtomPictureRegular()


class OrganismHeroTextHeaderRegular(NamedTuple):
    """
    Content page component - the text
    """
    id: str = ''
    title: str = ''
    text: str = ''
    author: str = ''
    date: str = ''


class OrganismArticleCookieRegular(NamedTuple):
    id: str = ''
    title: str = 'Cookie-Einstellungen'
    text: str = 'Ändern Sie hier Ihre Cookie-Einstellungen. Sie können auswählen, welche Kategorien von Cookies Sie (nicht) zulassen möchten.'


class OrganismContentHeroImageTitle(NamedTuple):
    id: str = ''
    classes: str = ''
    align: str = ''
    title: str = ''
    picture: AtomPictureRegular = AtomPictureRegular()
    link: AtomLinkRegular = AtomLinkRegular()


class OrganismContentPhotoMosaic(NamedTuple):
    id: str = ''
    figures: Sequence[AtomFigureRegular] = ()


class OrganismArticleRelatedItemsRegular(NamedTuple):
    """
    Basic/Content Page component
    Related item cards, based on chosen pages
    """
    title: str = ''
    cards: Iterable[MoleculeCardRegular] = ()
    tags: Iterable = ()
    variant: str = ''
    card_background: str = ''


class OrganismActualitiesLandingHeaderRegular(NamedTuple):
    """
    Actualities Landing Page component
    A simple header with text and a featured item (either news or event)
    """
    title: str = ''
    link_label: str = ''
    featured_item: MoleculeCardRegular = MoleculeCardRegular()
    excerpt: str = ''


class OrganismCardGridRegular(NamedTuple):
    id: str = ''
    title: str = ''
    cards: Sequence[MoleculeCardRegular] = ()


class OrganismExploreSearchHeader(NamedTuple):
    title: str = ''
    search_button_title: str = ''
    search_button_icon: str = 'custom/arrow-right-icon'


class OrganismObjectHeaderRegular(NamedTuple):
    title: str = ''
    subtitle: str = ''


class OrganismObjectIntro(NamedTuple):
    text: str = ''
    classes: str = ''

    def get_context_container(self):
        return 'text'
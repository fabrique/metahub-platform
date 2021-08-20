from typing import NamedTuple, Iterable, Sequence

from django.utils.translation import ugettext_lazy as _

from starling.interfaces.atoms import AtomPictureRegular as AtomPictureRegular, AtomFigureRegular, AtomLinkRegular

from ..atoms.interfaces import AtomVideoEmbedRegular
from ..molecules.interfaces import MoleculeObjectCardRegular, MoleculeAudioPlayer, \
    MoleculeCollectionCategoryCardRegular, MoleculeCardRegular


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

    def get_context_container(self):
        return 'text'


class OrganismContentDoubleLinkRichTextRegular(NamedTuple):
    id: str = ''
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
    title: str = ''
    text: str = ''
    button_change_text: str = _('Change settings')
    button_clear_text: str = _('Clear cookies')


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
    classes: str = ''
    cards: Iterable[MoleculeCardRegular] = ()
    tags: Iterable = ()
    variant: str = ''
    card_background: str = ''
    link: AtomLinkRegular = AtomLinkRegular()


class OrganismArticleRelatedItemsWithLinkRegular(OrganismArticleRelatedItemsRegular):
    """
    Basic/Content Page component
    Related item cards, based on chosen pages
    """
    link: AtomLinkRegular = AtomLinkRegular()


class OrganismFeaturedCardRegular(NamedTuple):
    """
    Actualities Landing Page component
    A simple header with text and a featured item (either news or event)
    """
    title: str = ''
    link_label: str = ''
    card: MoleculeCardRegular = MoleculeCardRegular()
    excerpt: str = ''


class OrganismFeaturedCardLinkToAllRegular(NamedTuple):
    """
    Home Page component
    A simple header with text and a featured item (either news or event)
    """
    title: str = ''
    link_label: str = ''
    card: MoleculeCardRegular = MoleculeCardRegular()
    excerpt: str = ''
    link: AtomLinkRegular = AtomLinkRegular()
    all_stories_link_label: str = ''


class OrganismCardGridRegular(NamedTuple):
    id: str = ''
    title: str = ''
    cards: Sequence[MoleculeCardRegular] = ()


class OrganismExploreSearchHeader(NamedTuple):
    title: str = ''
    search_button_title: str = ''
    search_button_icon: str = 'custom/arrow-right-icon'
    search_query: str = ''
    placeholder_text: str = ''
    main_filters: dict = {}


class OrganismObjectHeaderRegular(NamedTuple):
    title: str = ''
    subtitle: str = ''


class OrganismObjectIntroRegular(NamedTuple):
    text: str = ''
    classes: str = ''

    def get_context_container(self):
        return 'text'


class OrganismObjectMetadataRegular(NamedTuple):
    items: Sequence[dict] = ()


class OrganismSearchCardGridRegular(NamedTuple):
    cards: Sequence[MoleculeCardRegular] = ()


class OrganismHomeIntroRegular(NamedTuple):
    title: str = ''
    text: str = ''

    def get_context_container(self):
        return 'text'


class OrganismSponsorsRegular(NamedTuple):
    id: str = ''
    variant: str = 'default'
    title: str = ''
    text: str = ''
    logos: Iterable = ()

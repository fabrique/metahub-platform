from typing import NamedTuple, Iterable

from starling.interfaces.atoms import AtomPictureRegular as AtomPictureRegular, AtomFigureRegular, AtomLinkRegular

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
    video: AtomVideoEmbedRegular = AtomVideoEmbedRegular()
    caption: str = ''


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


class OrganismHeroHeaderSingleImageContentPageRegular(NamedTuple):
    """
    Content page component - just the image
    """
    id: str = ''
    picture: AtomPictureRegular = AtomPictureRegular()
    height: str = ''


class OrganismArticleCookieRegular(NamedTuple):
    id: str = ''
    title: str = 'Cookie-Einstellungen'
    text: str = 'Ändern Sie hier Ihre Cookie-Einstellungen. Sie können auswählen, welche Kategorien von Cookies Sie (nicht) zulassen möchten.'
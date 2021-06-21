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
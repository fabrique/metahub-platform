from starling.blocks.atoms.figure import AtomFigureRegularBlock
from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.blocks.atoms.picture import AtomPictureRegularBlock
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks
from wagtail.core.blocks import ListBlock

from .interfaces import *
from ..atoms.blocks import AtomVideoEmbedRegularBlock
from ..helpers import HelperRelatedPagesBlock
from ..molecules.blocks import MoleculeObjectCardRegularBlock, MoleculeContextCardRegularBlock, \
    MoleculeLinkRegularBlock, MoleculeAudioPlayerBlock, \
    MoleculeCollectionCategoryCardRegularBlock, MoleculeThemeHighlightRegularBlock, MoleculeObjectHighlightRegularBlock
from ..utils import count_words_html


class OrganismHeroImageHeaderRegularBlock(AdapterStructBlock):
    """
    Content Page Header Component
    Simple header with an image
    """
    picture = AtomPictureRegularBlock(resolution=Resolution(mobile="1920x1080"))

    class Meta:
        component = 'organisms.hero-image.regular'
        interface_class = OrganismHeroImageHeaderRegular


class OrganismHeroTextHeaderRegularBlock(AdapterStructBlock):
    """
    Content Page Header Component
    Header with text
    """
    title = blocks.CharBlock(max_length=200)
    text = blocks.TextBlock(max_length=2000)

    class Meta:
        component = 'organisms.hero-text.regular'
        interface_class = OrganismHeroTextHeaderRegular


class OrganismContentSingleRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a single richtext component
    """
    text = blocks.RichTextBlock()

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        defaults = {
            'id' : '',
        }
        component = 'organisms.article-content.regular'
        interface_class = OrganismContentSingleRichTextRegular


class OrganismContentSingleImageRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a single image with a caption
    """
    figure = AtomFigureRegularBlock([
        ('picture', AtomPictureRegularBlock(resolution=Resolution(mobile='1920', crop=True))),
    ])

    class Meta:
        defaults = {
            'id': '',
        }
        component = 'organisms.article-photo.regular'
        interface_class = OrganismContentSingleImageRegular


class OrganismContentSingleVideoRegularBlock(AdapterStructBlock):
    """
    Content Component
    Supports Vimeo and YouTube uploads. Includes an optional link to
    a video transcript for accessiblity purposes.
    """
    video = AtomVideoEmbedRegularBlock(required=True)
    caption = blocks.CharBlock(required=False)

    class Meta:
        defaults = {
            'id' : '',
        }
        component = 'organisms.article-video.regular'
        interface_class = OrganismContentSingleVideoRegular


class OrganismContentDoubleImageRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a richtext on the left and a picture with caption on the right.
    Optionally includes a link as well.
    """
    figure = AtomFigureRegularBlock()
    text = blocks.RichTextBlock(required=True)
    link = OptionalBlock(AtomLinkRegularBlock())

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        defaults = {}
        component = 'organisms.content-and-image.regular'
        interface_class = OrganismContentDoubleImageRichTextRegular


class OrganismContentHeroImageTitleBlock(AdapterStructBlock):
    """
    Content Component
    Image with title and link, call to action/highlight
    """
    title = blocks.CharBlock(max_length=200)
    link = AtomLinkRegularBlock()
    picture = AtomPictureRegularBlock()

    class Meta:
        defaults = {}
        component = 'organisms.hero-image-title.picture'
        interface_class = OrganismContentHeroImageTitle


class OrganismContentPhotoMosaicBlock(AdapterStructBlock):
    """
    Content Component
    A list of pictures placed playfully
    """
    figures = ListBlock(AtomFigureRegularBlock())

    class Meta:
        defaults = {}
        component = 'organisms.images.regular'
        interface_class = OrganismContentPhotoMosaic


class OrganismArticleCookieBlockRegular(AdapterStructBlock):

    title = blocks.CharBlock()
    text = blocks.TextBlock()

    class Meta:
        component = 'organisms.article-cookies.regular'
        interface_class = OrganismArticleCookieRegular


class OrganismArticleCuratedItemsRegularBlock(AdapterStructBlock):
    """
    Basic/Content Page component
    Allows linking to another page through clickable cards.
    """

    title = blocks.CharBlock(max_length=100)
    items = HelperRelatedPagesBlock()

    class Meta:
        label = "Gerelelateerde items (handgekozen)"
        icon = 'arrows-up-down'
        defaults = {}
        component = 'organisms.relevant-stories.be_cards'
        interface_class = OrganismArticleRelatedItemsRegular
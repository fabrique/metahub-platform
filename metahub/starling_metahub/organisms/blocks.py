from starling.blocks.atoms.figure import AtomFigureRegularBlock
from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.blocks.atoms.picture import AtomPictureRegularBlock
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks

from .interfaces import *
from ..atoms.blocks import AtomVideoEmbedRegularBlock
from ..molecules.blocks import MoleculeObjectCardRegularBlock, MoleculeContextCardRegularBlock, \
    MoleculeLinkRegularBlock, MoleculeAudioPlayerBlock, \
    MoleculeCollectionCategoryCardRegularBlock, MoleculeThemeHighlightRegularBlock, MoleculeObjectHighlightRegularBlock
from ..utils import count_words_html


class OrganismHeroHeaderSingleImageContentPageRegularBlock(AdapterStructBlock):
    """
    Content Page Header Component
    Simple header with 1 picture and a title
    """
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    picture = AtomPictureRegularBlock(resolution=Resolution(mobile='750', landscape='2048', crop=True))

    class Meta:
        component = 'organisms.simple-image-header.regular'
        interface_class = OrganismHeroHeaderSingleImageContentPageRegular


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
        component = 'organisms.article-video-embed.regular'
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
        defaults = {
            'id': '',
        }
        component = 'organisms.article-photos-and-text.regular'
        interface_class = OrganismContentDoubleImageRichTextRegular


class OrganismArticleCookieBlockRegular(AdapterStructBlock):

    title = blocks.CharBlock()
    text = blocks.TextBlock()

    class Meta:
        component = 'organisms.article-cookies.regular'
        interface_class = OrganismArticleCookieRegular
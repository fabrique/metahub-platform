from starling.blocks.atoms.figure import AtomFigureRegularBlock
from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.blocks.atoms.picture import AtomPictureRegularBlock
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks

from .unused_interfaces import *
from ..atoms.blocks import AtomVideoEmbedRegularBlock
from ..molecules.blocks import MoleculeObjectCardRegularBlock, MoleculeContextCardRegularBlock, \
    MoleculeLinkRegularBlock, MoleculeAudioPlayerBlock, \
    MoleculeCollectionCategoryCardRegularBlock, MoleculeThemeHighlightRegularBlock, MoleculeObjectHighlightRegularBlock
from ..utils import count_words_html

class OrganismSearchHeaderRegularBlock(AdapterStructBlock):
    """
    Homepage Component, SearchPage Component
    Header containing a background of alternating images. It also has a search
    bar that features livesearch.
    """
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=True)
    pictures = blocks.ListBlock(AtomPictureRegularBlock(resolution=Resolution(mobile='750', landscape='2048', crop=True)))

    def build_extra(self, value, build_args, parent_context=None):
        build_args['live_search_url'] = parent_context.get('live_search_url','')
        build_args['search_url'] = parent_context.get('search_url', '')
        build_args['picture_index'] = parent_context.get('picture_index', 0)
        build_args['variant'] = parent_context.get('variant','default')
        build_args['is_homepage'] = parent_context.get('is_homepage', False)

    class Meta:
        defaults = {'live_search_url':'sumtin'}
        component = 'organisms.search-header.regular'
        interface_class = OrganismSearchHeaderRegular


class OrganismThemeHighlightsRegularBlock(AdapterStructBlock):
    """
    Homepage Component
    Renders a block containing alternating "slides" with highlighted stories,
    representing the themes of the collection. The specific content is inherited
    from the story pages and not entered here.
    """
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=True)
    theme_categories = blocks.ListBlock(blocks.CharBlock(required=True))
    themes = blocks.ListBlock(MoleculeThemeHighlightRegularBlock())


class OrganismObjectHighlightsRegularBlock(AdapterStructBlock):
    """
    Homepage Component
    Renders a somewhat mosaic style of objects that are currently the highlights
    of the collection.  Note that content amount isn't limited here, but the page
    model will not return anything but the first 3.
    """
    title = blocks.CharBlock(required=True)
    introduction = blocks.RichTextBlock(required=True)
    highlights = blocks.ListBlock(MoleculeObjectHighlightRegularBlock())


class OrganismCollectionCategoriesRegularBlock(AdapterStructBlock):
    """
    Homepage Component
    Mimics the design of the original block on the Typo3 website that
    outlines the museums primary collection domains. Essentially just
    a list of cards.
    """
    title = blocks.CharBlock(required=True)
    cards = blocks.ListBlock(MoleculeCollectionCategoryCardRegularBlock())

    class Meta:
        defaults = {}
        component = 'organisms.card-grid.regular'
        interface_class = OrganismCollectionCategoriesRegular


class OrganismHeroHeaderVideoRegularBlock(AdapterStructBlock):
    """
    Header Component
    Not currently used, because MetaHub does not have video content yet.
    """
    title = blocks.CharBlock(required=True)
    video = AtomVideoEmbedRegularBlock(required=True)

    class Meta:
        defaults = {
            'id' : '',
        }
        component = 'organisms.logo-marquee.regular'
        interface_class = OrganismHeroHeaderVideoRegular



class OrganismHeroHeaderMultiImageRegularBlock(AdapterStructBlock):
    """
    Header Component
    Hero header that allows for multiple images to be picked. These will
    become part of a slideshow that can be opened through the header. They are also
    inherited by the intro component on MetaHub pages, which will in addition mimic
    slide behaviour.
    """
    # show_fullscreen_button = blocks.BooleanBlock(default=True, required=False)
    pictures = blocks.ListBlock(AtomPictureRegularBlock(resolution=Resolution(mobile='750', landscape='2048', crop=True)))

    class Meta:
        defaults = {
            'id' : '',
            'theme' : 'blue',
        }
        component = 'organisms.image-header.regular'
        interface_class = OrganismHeroHeaderMultiImageRegular


class OrganismContextDiscoveryChoiceRegularBlock(AdapterStructBlock):
    """
    Header Component
    Allows the user to choose elements for the context ribbon. Note that
    content amount isn't limited here, but the page model will not
    return anything but the first 3.
    """
    cards = blocks.ListBlock(MoleculeContextCardRegularBlock())

    class Meta:
        defaults = {
            'title' : 'Entdecken Sie das Werk im Kontext',
            'id': '',
        }
        component = 'organisms.context-cards.regular'
        interface_class = OrganismObjectMosaicChoiceRegular


class OrganismContentDoubleQuoteRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a quote in the left column, accompanied by a text block on
    the right.
    """
    quote = blocks.CharBlock(required=True)
    attribution = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=True)

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        defaults = {
            'id': '',
        }
        component = 'organisms.article-quote-and-text.regular'
        interface_class = OrganismContentDoubleQuoteRichTextRegular

class OrganismObjectMosaicChoiceRegularBlock(AdapterStructBlock):
    """
    Content Component
    This is the variant for the story page where they can be picked,
    on the object page it is generated. It is not currently used as
    the series pages is intended to fulfill this role for now.
    """
    title = blocks.CharBlock(required=False)
    cards = blocks.ListBlock(MoleculeObjectCardRegularBlock())


class OrganismLinkListRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a link block for relevant links on the topic of a story or object.
    """
    title = blocks.CharBlock(required=False)
    links = blocks.ListBlock(AtomLinkRegularBlock())

    class Meta:
        defaults = {
            'id': '',
        }
        component = 'organisms.article-links.regular'
        interface_class = OrganismLinkListRegular


class OrganismContentSingleAudioRegularBlock(AdapterStructBlock):
    """
    Content Component
    Regular audio player component for the content body. Accessibility
    guidelines mandate this includes an audio transcript.
    """
    audio_fragment = MoleculeAudioPlayerBlock()

    class Meta:
        defaults = {}
        component = 'organisms.article-audio.regular'
        interface_class = OrganismContentSingleAudioRegular
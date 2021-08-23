from django.utils.translation import ugettext_lazy as _
from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.blocks.atoms.picture import AtomPictureRegularBlock
from starling.blocks.helpers import HelperHrefBlock
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock

from ..helpers import (HelperDocumentBlock, HelperHrefBlockSimple,
                       HelperOptionalHrefBlock, HelperPageURLBlock)
from .interfaces import *


class MoleculeObjectCardRegularBlock(AdapterStructBlock):
    page = blocks.PageChooserBlock(required=False, target_model='collection.MetaHubObjectPage')


class MoleculeThemeHighlightRegularBlock(AdapterStructBlock):
    """
    Represents a chosen highlighted story shown on the homepage.
    Does not have its own interface, rather the page and intro text are resolved
    in the page model to return the correct components.
    """
    page = blocks.PageChooserBlock(target_model=('collection.MetaHubStoryPage'))
    intro_text = blocks.TextBlock(required=False, help_text='Leave blank to use the text of the story page')


class MoleculeObjectHighlightRegularBlock(AdapterStructBlock):
    """
    Represents a chosen highlighted object or object series of the homepage.
    Does not have its own interface, rather the page and intro text are resolved
    in the page model to return the correct components.
    """
    page = blocks.PageChooserBlock(target_model=('collection.MetaHubObjectPage'))
    intro_text = blocks.TextBlock(required=False, help_text='Leave blank to use the text of the object page')


class MoleculeCollectionCategoryCardRegularBlock(AdapterStructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=True)
    image = AtomPictureRegularBlock(required=True)
    href = HelperHrefBlockSimple()

    class Meta:
        component = 'molecules.collection_category.regular'
        interface_class = MoleculeCollectionCategoryCardRegular


class MoleculeContextCardRegularBlock(AdapterStructBlock):
    page = PageChooserBlock(target_model=('stories.MetaHubStoryPage', 'collection.MetaHubObjectPage', 'collection.MetaHubObjectSeriesPage'))

    class Meta:
        defaults = {}
        component = 'molecules.card.regular'
        interface_class = MoleculeContextCardRegular


class MoleculeLinkRegularBlock(AdapterStructBlock):
    page_href = HelperHrefBlock()
    title = blocks.CharBlock()

    class Meta:
        defaults = {

        }
        component = 'molecules.card.regular'
        interface_class = MoleculeLinkRegular


class MoleculeLinkListRegularBlock(AdapterStructBlock):
    links = blocks.ListBlock(AtomLinkRegularBlock())

    class Meta:
        defaults = {
            'title' : '',
            'classes' : '',
            'direction': 'vertical',
        }
        component = 'molecules.link-list.regular'
        interface_class = MoleculeLinkListRegular


class MoleculeAudioPlayerBlock(AdapterStructBlock):
    title = blocks.CharBlock()
    file_title = blocks.CharBlock()
    file_subtitle = blocks.CharBlock()
    file = HelperDocumentBlock()
    audio_transcript = HelperOptionalHrefBlock(blank=True)

    class Meta:
        defaults = {}
        component = 'molecules.audio.regular'
        interface_class = MoleculeAudioPlayer


class MoleculeLogoRegularBlock(AdapterStructBlock):
    PICTURE_SIZE_PERCENTAGES = [(x, x) for x in range(10, 100, 10)]

    picture = AtomPictureRegularBlock(resolution=Resolution(mobile='160x80', crop=False))
    size_percentage = blocks.ChoiceBlock(required=False, choices=PICTURE_SIZE_PERCENTAGES, label=_('Size in percentage'))
    link = AtomLinkRegularBlock()

    def build_extra(self, value, build_args, parent_context=None):
        picture = value.get('picture', None)
        link = build_args.pop('link', None)
        build_args.update({
            'href': (getattr(link, 'href', None) if link else None),
            'picture': (AtomPictureRegular(**Resolution(mobile='360x180', crop=False).resolve(picture.get('source')))
                            if picture and parent_context.get('variant') not in ['', 'default'] else build_args.get('picture'))
        })

    class Meta:
        defaults = {}
        component = 'molecules.logo.regular'
        interface_class = MoleculeLogoRegular
        label = _('Logo')

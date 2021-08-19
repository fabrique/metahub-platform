from starling.blocks.atoms.picture import AtomPictureBlock, AtomPictureRegularBlock
from starling.blocks.helpers import HelperHrefBlock
from starling.interfaces.atoms import AtomLinkRegular, AtomFigureRegular
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock
from wagtail.core import blocks

from ..atoms.interfaces import AtomVideoEmbedRegular
from ..helpers import HelperEmbedBlock, HelperPageURLBlock, HelperOptionalHrefBlock


class AtomVideoEmbedRegularBlock(AdapterStructBlock):
    video = HelperEmbedBlock()
    picture = AtomPictureRegularBlock(resolution=Resolution(mobile="1080x1050", crop=True))

    class Meta:
        defaults = {
            'classes': '',
            'autoplay': False,
        }
        interface_class = AtomVideoEmbedRegular


class AtomTitlelessLinkRegularBlock(AdapterStructBlock):
    href = HelperPageURLBlock()
    icon_before = blocks.CharBlock()
    icon_after = blocks.CharBlock()
    classes = blocks.CharBlock(required=False)

    class Meta:
        defaults = {
            'title' : '',
            'icon_before': '',
            'icon_after': '',
            'long_title': '',
            'classes': '',
            'target': '',
        }
        interface_class = AtomLinkRegular


class AtomFigureRegularBlockHighRes(AdapterStructBlock):
    picture = AtomPictureRegularBlock(resolution=Resolution("4096"), crop=False)
    caption = blocks.CharBlock(required=False)
    classes = blocks.CharBlock(required=False)

    class Meta:
        defaults = {'classes': ''}
        interface_class = AtomFigureRegular
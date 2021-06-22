from starling.blocks.atoms.picture import AtomPictureBlock, AtomPictureRegularBlock
from starling.blocks.helpers import HelperHrefBlock
from starling.interfaces.atoms import AtomLinkRegular
from starling.mixins import AdapterStructBlock
from wagtail.core import blocks

from ..atoms.interfaces import AtomVideoEmbedRegular
from ..helpers import HelperEmbedBlock, HelperPageURLBlock, HelperOptionalHrefBlock


class AtomVideoEmbedRegularBlock(AdapterStructBlock):
    video = HelperEmbedBlock()
    picture = AtomPictureRegularBlock()

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



from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks

from .interfaces import *
from ..molecules.blocks import MoleculeLinkListRegularBlock


class QuarkFooterBarColumnBlock(AdapterStructBlock):
    title = blocks.CharBlock()
    link_list = MoleculeLinkListRegularBlock()

    class Meta:
        defaults = {}
        interface_class = QuarkFooterBarColumn
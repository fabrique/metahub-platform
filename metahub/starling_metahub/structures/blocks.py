from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.mixins import AdapterStructBlock
from wagtail.core import blocks
from .interfaces import *

class StructureFooterBarSimpleBlock(AdapterStructBlock):
    links = blocks.ListBlock(AtomLinkRegularBlock())

    class Meta:
        defaults = {}
        component = 'structures.footer-bar.simple'
        interface_class = StructureFooterBarSimple
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from embed_video.backends import detect_backend, UnknownBackendException, VimeoBackend, YoutubeBackend
from fabrique.vimeo.blocks import VimeoBlock
from fabrique.youtube.blocks import YouTubeBlock
from starling.interfaces.generic import Resolution
from starling.mixins import HelperMixin
from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock, StructBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class HelperPageURLBlock(HelperMixin, PageChooserBlock):
    def to_params(self, value, field_name) -> dict:
        return {self.meta.field: value.url}
    class Meta:
        field = 'href'


class HelperImageURLBlock(HelperMixin, ImageChooserBlock):
    """ Helper to select a video for a QuarkVideoSourceBlock """
    def to_params(self, value, field_name) -> dict:
        return {
            self.meta.field: value.get_rendition(
                f'fill-{self.meta.resolution.mobile}').url}
    class Meta:
        field = 'src'
        resolution = Resolution('200x200')


class HelperOptionalHrefBlock(HelperMixin, blocks.StructBlock):
    """ Helper to make all kinds of urls. """

    source = blocks.StreamBlock(
        [
            ('page', PageChooserBlock()),
            ('external', blocks.URLBlock()),
        ],
        blank=True
    )

    def to_params(self, value, field_name: str = 'href') -> dict:
        child = value['source'][0]
        name = child.block.name

        if name == 'page':
            return {field_name: child.value.url}

        if name == 'external':
            return {field_name: child.value, 'target': '_blank'}

        raise ValueError(f'Unknown link type {name}')


class HelperEmbedBlock(HelperMixin, StructBlock):
    """ Helper to convert a url to video parameters """
    src = blocks.StreamBlock(
        [
            ('youtube', YouTubeBlock([
                ('src', blocks.URLBlock(role='source')),
            ])),
            ('vimeo', VimeoBlock([
                ('src', blocks.URLBlock(role='source')),
            ])),
        ],
        min_num=1, max_num=1,
    )

    def clean(self, value):
        value = super().clean(value)
        url = self._get_url(value)
        try:
            detect_backend(url)
        except UnknownBackendException as e:
            raise ValidationError(
                'Validation error in Embed block',
                params=[ErrorList[e]])
        return value

    def to_params(self, value, field_name) -> dict:
        url = self._get_url(value)
        backend = detect_backend(url)
        return {
            'href': url,
            'video_id': backend.code,
            'video_type': {
                VimeoBackend: 'vimeo',
                YoutubeBackend: 'youtube',
            }.get(backend.__class__),
        }

    def _get_url(self, value):
        return value['src'][0].value['src']




class HelperHrefBlockDocument(HelperMixin, blocks.StructBlock):
    """ Helper to make all kinds of urls. """

    source = blocks.StreamBlock(
        [
            ('page', PageChooserBlock()),
            ('external', blocks.URLBlock()),
            ('mail', blocks.EmailBlock()),
            ('phone', blocks.CharBlock()),
            ('document', DocumentChooserBlock())
        ],
        min_num=1,
        max_num=1,
    )

    def to_params(self, value, field_name: str = 'href') -> dict:
        child = value['source'][0]
        name = child.block.name

        if name == 'page':
            return {field_name: child.value.url}

        if name == 'external':
            return {field_name: child.value, 'target': '_blank'}

        if name == 'mail':
            return {field_name: f'mailto:{child.value}'}

        if name == 'phone':
            return {field_name: f'tel:{child.value}'}

        if name == 'document':
            return {field_name: child.value.url}

        raise ValueError(f'Unknown link type {name}')


class HelperHrefBlockSimple(HelperMixin, blocks.StructBlock):
    """ Helper to make all external or internal urls """

    source = blocks.StreamBlock(
        [
            ('page', PageChooserBlock()),
            ('external_open_in_same', blocks.URLBlock()),
            ('external_open_in_new', blocks.URLBlock()),
        ],
        min_num=1,
        max_num=1,
    )

    def to_params(self, value, field_name: str = 'href') -> dict:
        child = value['source'][0]
        name = child.block.name

        if name == 'page':
            return {field_name: child.value.url}

        if name == 'external_open_in_same':
            return {field_name: child.value }

        if name == 'external_open_in_new':
            return {field_name: child.value, 'target': '_blank'}

        raise ValueError(f'Unknown link type {name}')


class HelperDocumentBlock(HelperMixin, blocks.StructBlock):
    source = blocks.StreamBlock(
        [
            ('document', DocumentChooserBlock())
        ],
        min_num=1,
        max_num=1,
    )

    def to_params(self, value, field_name: str = 'source') -> dict:
        child = value['source'][0]
        name = child.block.name

        if name == 'document':
            return {field_name: child.value.url}

        raise ValueError(f'Unknown source type {name}')

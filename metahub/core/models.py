from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea
from starling.interfaces.atoms import AtomLinkRegular, AtomPictureRegular
from starling.interfaces.generic import Resolution

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index

from .mixins import PagePromoMixin
from .utils import MetaHubThemeColor, format_date
from ..starling_metahub.molecules.interfaces import MoleculeCardRegular

from ..starling_metahub.structures.blocks import StructureFooterBarSimpleBlock


class MetaHubBasePage(PagePromoMixin, Page):
    """
    Base page for all MetaHub online collection pages
    """

    theme_color = models.CharField(choices=MetaHubThemeColor.choices,
                                   default=MetaHubThemeColor.MAGENTA,
                                   max_length=100)

    def get_content_with_numbered_captioned_entities(self):
        children = []
        caption_count = 1

        for child in self.content:
            if child.block.name == 'double_picture_richtext':
                if child.value:
                    caption = child.value['figure']['caption']

                    if len(caption):
                        child.value['figure']['caption'] = f'({caption_count}) {caption}'
                        caption_count += 1

            elif child.block.name == 'video':
                if child.value:
                    caption = child.value['caption']
                    if len(caption):
                        child.value['caption'] = f'({caption_count}) {caption}'
                        caption_count += 1

            elif child.block.name == 'image_mosaic':
                if child.value:
                    figures = child.value['figures']
                    for figure in figures:
                        caption = figure['caption']
                        if len(caption):
                            figure['caption'] = f'({caption_count}) {caption}'
                            caption_count += 1

            # This might be superfluous to have it be another list
            children.append(child)
        return children

    def get_page_header_image(self):
        """ Used in the card representation.
        TODO: Optional override through promo img? """
        if hasattr(self, 'hero_header') and len(self.hero_header):
            picture_structvalue = self.hero_header[0].value['picture']
            return AtomPictureRegular(**Resolution(mobile='1920', crop=True).resolve(picture_structvalue['source']))

    def get_page_date(self):
        if hasattr(self, 'date') and (date := getattr(self, 'date')):
            return date

    def get_page_authors(self):
        if hasattr(self, 'authors') and (authors := getattr(self, 'authors')):
            return [str(author) for author in authors]
        return []

    def get_page_label(self):
        return ''

    def get_page_related_items(self):
        return []

    def get_card_representation(self):
        return MoleculeCardRegular(
            title=self.title,
            label=self.get_page_label(),
            href=self.url,
            picture=self.specific.get_page_header_image(),
            date=format_date(self.specific.get_page_date())
        )

    def time_relevance(self):
        pass

    class Meta:
        abstract = True


class MetahubImage(Image):
    alt_text = models.CharField(
        'Alt tekst',
        help_text="Optionele beschrijving van wat er in de afbeelding te zien is.",
        max_length=150,
        blank=True)

    attribution = models.CharField(
        'Credit',
        help_text="Artist credit or licensing information, leave blank if not applicable",
        max_length=4000,
        blank=True
    )

    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'attribution',
    )

    search_fields = list(Image.search_fields) + [
        index.SearchField('alt_text'),
        index.SearchField('attribution'),
    ]

    @property
    def relative_focal_point_x(self):
        if not self.focal_point_x:
            return .5
        # relative position
        relative_x = self.focal_point_x / self.width
        focal_correction = self.focal_point_width * relative_x
        if relative_x > .5:
            # correct towards right
            corrected_x = self.focal_point_x - ((self.focal_point_width / 2) - focal_correction)
        else:
            # correct towards left
            corrected_x = self.focal_point_x + ((self.focal_point_width / 2) - focal_correction)
        corrected_relative_x = corrected_x / self.width
        return corrected_relative_x

    @property
    def relative_focal_point_y(self):
        if not self.focal_point_y:
            return .5
        relative_y = self.focal_point_y / self.height
        focal_correction = self.focal_point_height * relative_y
        if relative_y > .5:
            # correct towards right
            corrected_y = self.focal_point_y - ((self.focal_point_height / 2) - focal_correction)
        else:
            # correct towards left
            corrected_y = self.focal_point_y + ((self.focal_point_height / 2) - focal_correction)
        corrected_relative_y = corrected_y / self.height
        return corrected_relative_y

    @property
    def relative_focal_point_percent(self):
        return '{}% {}%'.format(int(self.relative_focal_point_x * 100), int(self.relative_focal_point_y * 100))


@register_setting
class GlobalSettings(BaseSetting):
    """
    Global settings
    """
    default_share_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        verbose_name="Standaard share image",
        null=True,
        blank=True,
        help_text=_("Afbeelding voor op Facebook e.d. voor pagina\'s die zelf geen afbeelding hebben."),
        on_delete=models.SET_NULL,
        related_name='+'
    )

    default_site_description = models.CharField(
        blank=True,
        max_length=300,
        verbose_name="Meta description",
        help_text=_("Beschrijving van de site voor zoekmachine's e.d.")
    )

    footer_content_simple = StreamField(
        [('footer', StructureFooterBarSimpleBlock())]
    )

    def get_contextual_footer(self):
        if self.footer_content_simple:
            component = self.footer_content_simple[0].block.build_component(self.footer_content_simple[0].value)
            component = component._replace(context=True)
            return component

    def get_content_page_footer(self):
        if self.footer_content_simple:
            component = self.footer_content_simple[0].block.build_component(self.footer_content_simple[0].value)
            component = component._replace(content_page=True)
            return component

    panels = [
        ImageChooserPanel('default_share_image'),
        FieldPanel('default_site_description', classname="fullwidth", widget=Textarea(attrs={'rows': 2})),
        StreamFieldPanel('footer_content_simple'),
    ]

    class Meta:
        verbose_name = 'Algemene instellingen'
        verbose_name_plural = 'Algemene instellingen'


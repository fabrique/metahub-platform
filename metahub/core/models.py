from itertools import chain

from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index

from .mixins import PagePromoMixin

from ..starling_metahub.structures.blocks import StructureFooterBarSimpleBlock


class MetaHubBasePage(PagePromoMixin, Page):
    """
    Base page for all MetaHub online collection pages
    """
    # def get_my_collection_url(self):
    #     from metahub.my_collection.models import MetaHubMyCollectionPage
    #     my_collection = MetaHubMyCollectionPage.objects.live().first()
    #     if my_collection:
    #         return my_collection.url
    #     return '/'
    #
    # def get_search_base_url(self):
    #     """
    #     Used by the tags that redirect to search with a predefined param
    #     as well as the object series "see all objects in this series"
    #     """
    #     from metahub.search.models import MetaHubSearchPage
    #     search =  MetaHubSearchPage.objects.live().first()
    #     if search:
    #         return search.search_url()
    #     return '/'
    #
    # def get_highlights(self):
    #     """
    #     Checks for each page type what pages have been marked as
    #     highlights and creates a card representation to show.
    #     """
    #     cards = []
    #
    #     # To avoid circular imports
    #     from metahub.collection.models.object_page import MetaHubObjectPage
    #     from metahub.collection.models.object_series_page import MetaHubObjectSeriesPage
    #     from metahub.stories.models import MetaHubStoryPage
    #
    #     obj_highlights = MetaHubObjectPage.objects.all().specific().live().filter(is_highlight=True)
    #     obj_series_highlights = MetaHubObjectSeriesPage.objects.all().specific().live().filter(is_highlight=True)
    #     story_highlights = MetaHubStoryPage.objects.all().specific().live().filter(is_highlight=True)
    #
    #     all_highlights = list(chain(obj_highlights, obj_series_highlights, story_highlights))
    #
    #     for highlight in all_highlights:
    #         cards.append(highlight.get_search_representation())
    #
    #     return cards

    class Meta:
        abstract = True


class AbstractMetaHubRichBasePage(MetaHubBasePage):

    parent_page_types = ['collection.MetaHubCategoryOverviewPage']

    class Meta:
        abstract = True

    # Defines the broader category of this page, for example "artwork" or "family legacy"
    # collection_category = models.ForeignKey(
    #     CollectionCategory,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
    #     blank=True
    # )
    #
    # is_highlight = models.BooleanField(blank=True, default=False)
    #
    # # Intro that is used on the homepage
    # highlight_intro = models.TextField(max_length=4096, blank=True, default='')
    #
    # # Text of the introduction component
    # intro = models.TextField(max_length=4096, blank=True)
    # reading_time = models.PositiveIntegerField(default=0, null=True, blank=True)
    # show_reading_time = models.BooleanField(default=False)
    # audio = StreamField([('audio', MoleculeAudioPlayerBlock())], blank=True)
    #
    # # Main content block, differs per subclass
    # content = StreamField([])
    #
    # # Cards at the bottom of the page, can be a link to a story or object
    # discover_in_context = StreamField([
    #     ('card_list', OrganismContextDiscoveryChoiceRegularBlock())
    # ], blank=True)
    #
    # content_panels = MetahubBasePage.content_panels + [
    #     StreamFieldPanel('discover_in_context'),
    #     MultiFieldPanel([
    #         FieldPanel('is_highlight'),
    #         FieldPanel('highlight_intro')
    #     ]),
    #     MultiFieldPanel([
    #         FieldPanel('intro'),
    #         FieldPanel('show_reading_time'),
    #         StreamFieldPanel('audio')
    #     ], "Sub header")
    # ]
    #
    # def get_category(self):
    #     """
    #     Stringified version of the page's category (Objekt, Geschichten, Series etc.)
    #     """
    #     try:
    #         return str(self.collection_category)
    #     except AttributeError:
    #         return ''
    #
    # def estimate_reading_time(self):
    #     if self.show_reading_time:
    #         word_count = 0
    #
    #         for stream_child in self.content:
    #             try:
    #                 word_count += stream_child.block.get_word_count(stream_child.value)
    #             except AttributeError:
    #                 pass
    #
    #         return str(1 + word_count // 200)
    #
    # def has_context(self):
    #     """
    #     Checks whether the context ribbon should be shown, based on if there is
    #     any context defined in the CMS. Passed on to the template to trigger
    #     correct layout.
    #     """
    #     try:
    #         self.discover_in_context[0]
    #     except IndexError:
    #         return False
    #     return True
    #
    # def build_context_cards(self):
    #     """
    #     If context cards were chosen, build the right ones. Each page defines its
    #     own method to render the correct card which we can use.
    #     """
    #     cards = []
    #     if self.has_context():
    #         organism_cards = self.discover_in_context[0]
    #         for card in organism_cards.value['cards']:
    #             if card['page']:
    #                 page = card['page'].specific
    #                 cards.append(page.get_card_representation())
    #         return cards[:3]
    #     else:
    #         return cards
    #
    # def build_intro(self):
    #     """
    #     Builds the correct intro component based on the type of hero component.
    #     Originally intended to support both video and image. At the moment the
    #     museum has no video content so this always returns the picture variant.
    #     """
    #     return self.build_picture_intro()
    #
    # def build_picture_intro(self):
    #     """
    #     Build the intro component based on the images that were uploaded into the
    #     hero image header.
    #     """
    #     pictures = self.get_hero_images()
    #     description = {'text': self.intro }
    #     component = OrganismImageIntroRegular(reading_time=self.reading_time,
    #                                           pictures=pictures,
    #                                           description=description,
    #                                           type='',
    #                                           audio=self.get_audio(),
    #                                           information=self.get_hero_info(),
    #                                           minimal=self.has_no_rich_content(),
    #                                           favinfo=self.get_favourite_info()
    #                                           )
    #     return component
    #
    # def has_no_rich_content(self):
    #     """
    #     Checks whether any non-automatically generated content is present. Determines
    #     whether the minimal layout variant should be triggered in template.
    #     """
    #
    #     try:
    #         self.content[0]
    #     except IndexError:
    #         no_body_content = True
    #     else:
    #         no_body_content = False
    #
    #     if not self.intro:
    #         no_intro_content = True
    #     else:
    #         no_intro_content = False
    #
    #     return no_body_content and no_intro_content
    #
    # def get_audio(self):
    #     """
    #     The intro component supports an audio fragment. Takes the audio fragment
    #     from the CMS if any was chosen and returns this so the intro can use it.
    #     """
    #     try:
    #         audio_child = self.audio[0]
    #     except IndexError:
    #         return None
    #     else:
    #         return audio_child.block.build_component(audio_child.value)
    #
    # def get_lightbox_items(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_lightbox_items on the subclass')
    #
    # def get_search_representation(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_search_representation on the subclass')
    #
    #
    # def get_card_representation(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_card_representation on the subclass')
    #
    # def build_hero_header(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement build_hero_header on the subclass')
    #
    # def get_hero_images(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_hero_images on the subclass')
    #
    # def get_hero_info(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_hero_info on the subclass')
    #
    # def get_primary_image(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_primary_image on the subclass')
    #
    # def get_raw_images(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_raw_image on the subclass')
    #
    # def get_tags_as_list(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_tags_as_list on the subclass')
    #
    # def get_favourite_info(self):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement get_favourite_info on the subclass')
    #
    # def is_favourite(self, request):
    #     """
    #     Needs to be overridden and implemented by subclass.
    #     """
    #     raise NotImplementedError('You need to implement is_favourite on the subclass')
    #
    # def get_promo_image(self):
    #     return self.get_primary_image()
    #
    # def save(self, *args, **kwargs):
    #     self.reading_time = self.estimate_reading_time()
    #     super().save(**kwargs)


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


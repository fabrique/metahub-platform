from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtailmodelchooser.blocks import ModelChooserBlock

from metahub.content.blocks import content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.molecules.interfaces import MoleculeCardRegular, MoleculeExploreCardRegular
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismHeroTextHeaderExtraInfoBlock, OrganismArticleCuratedItemsRegularBlock, \
    OrganismArticleRelatedItemsRegularBlock, OrganismArticleCuratedStoriesRegularBlock, \
    OrganismArticleRelatedStoriesRegularBlock


class MetaHubLocationPage(MetaHubBasePage):
    """
    Page for the locations. These pages are not based on BeeCollect data but all
    made in the CMS. Location is basically the same as a story page.
    """
    parent_page_types = ['overviews.MetaHubOverviewPage']

    authors = StreamField([
        ('author', ModelChooserBlock(target_model='authors.Author'))
    ], blank=True)

    date = models.DateField(blank=True, null=True)
    latitude = models.CharField(blank=True, max_length=200)
    longitude = models.CharField(blank=True, max_length=200)

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ])
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderExtraInfoBlock()),
    ])

    content = StreamField(content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedStoriesRegularBlock()),
        ('related_automatic', OrganismArticleRelatedStoriesRegularBlock()),

    ], blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        MultiFieldPanel([
            FieldPanel('date'),
            StreamFieldPanel('authors'),
            MultiFieldPanel([
                FieldPanel('latitude'),
                FieldPanel('longitude')
            ], heading="Location specifics")
        ], heading="Publishing information"),
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading="Header"),
        StreamFieldPanel('content'),
        StreamFieldPanel('related_items')
    ]

    def get_page_related_items(self):
        return MetaHubLocationPage.objects.live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return 'Location'

    def get_page_type(self):
        return 'story' # uses same card renderings

    def get_card_representation(self):
        return MoleculeExploreCardRegular(
            title=self.title,
            label=self.get_page_label(),
            subtitle="TODO wat komt hier?",
            href=self.url,
            picture=self.get_page_header_image(),
            type=self.get_page_type(),
            theme_color=self.theme_color
        )
    #
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtailmodelchooser.blocks import ModelChooserBlock

from metahub.content.blocks import rich_collection_entity_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.molecules.interfaces import MoleculeExploreCardRegular
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismHeroTextHeaderExtraInfoBlock, OrganismArticleCuratedStoriesRegularBlock, \
    OrganismArticleRelatedStoriesRegularBlock


class MetaHubStoryPage(MetaHubBasePage):
    """
    Page for the stories. These pages are not based on BeeCollect data but all
    made in the CMS.
    """
    parent_page_types = ['overviews.MetaHubOverviewPage']

    authors = StreamField([
        ('author', ModelChooserBlock(target_model='authors.Author'))
    ], blank=True)

    date = models.DateField(blank=True, null=True)

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ])
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderExtraInfoBlock()),
    ])

    content = StreamField(rich_collection_entity_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedStoriesRegularBlock()),
        ('related_automatic', OrganismArticleRelatedStoriesRegularBlock()),

    ], blank=True)

    tags = ClusterTaggableManager(through='stories.StoryTag', blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        MultiFieldPanel([
            FieldPanel('date'),
            StreamFieldPanel('authors'),
        ], heading="Publishing information"),
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading="Header"),
        StreamFieldPanel('content'),
        StreamFieldPanel('related_items'),
        FieldPanel('tags')
    ]

    def get_page_related_items(self):
        return MetaHubStoryPage.objects.live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return _('Story')

    def get_card_representation(self):
        return MoleculeExploreCardRegular(
            title=self.title,
            label=self.get_page_label(),
            subtitle="TODO wat komt hier?",
            href=self.url,
            picture=self.get_page_header_image(),
            type='story',
            theme_color=self.theme_color
        )
    #
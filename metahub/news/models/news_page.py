from django.db import models
from django.utils.timezone import now
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtailmodelchooser.blocks import ModelChooserBlock

from metahub.content.blocks import content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismHeroTextHeaderRegularBlock, OrganismArticleCuratedItemsRegularBlock, OrganismHeroTextHeaderExtraInfoBlock, \
    OrganismArticleRelatedItemsRegularBlock


class MetaHubNewsPage(MetaHubBasePage):
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

    content = StreamField(content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedItemsRegularBlock()),
        ('related_automatic', OrganismArticleRelatedItemsRegularBlock()),

    ], blank=True)

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
        StreamFieldPanel('related_items')
    ]

    def get_page_related_items(self):
        return MetaHubNewsPage.objects.live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return 'News'

    def time_relevance(self):
        return abs(int(now().timestamp() - int(self.date.strftime('%s'))))
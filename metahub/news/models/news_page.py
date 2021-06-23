from django.db import models
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
    ], blank=True)
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderExtraInfoBlock()),
    ])

    content = StreamField(content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedItemsRegularBlock()),
        ('related_automatic', OrganismArticleRelatedItemsRegularBlock()),

    ], blank=True)

    content_panels = MetaHubBasePage.content_panels + [
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

    def get_page_date(self):
        return self.date

    def get_page_authors(self):
        if len(self.authors):
            return [str(author) for author in self.authors]

    def get_page_related_items(self):
        return MetaHubNewsPage.objects.all().live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return 'News'
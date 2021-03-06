from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.utils.timezone import now
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField

from metahub.content.blocks import cookieless_content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismArticleCuratedItemsRegularBlock, OrganismHeroTextHeaderExtraInfoBlock, \
    OrganismArticleRelatedItemsRegularBlock


class MetaHubEventPage(MetaHubBasePage):
    parent_page_types = ['news.MetaHubActualitiesLandingPage']

    date = models.DateField(null=True)
    event_location = models.CharField(blank=True, null=True, default='', max_length=200)

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ])
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderExtraInfoBlock()),
    ])

    content = StreamField(cookieless_content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedItemsRegularBlock()),
        ('related_automatic', OrganismArticleRelatedItemsRegularBlock()),

    ], blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('event_location')
        ], heading="Event information"),
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading="Header"),
        StreamFieldPanel('content'),
        StreamFieldPanel('related_items')
    ]

    def get_page_related_items(self):
        return MetaHubEventPage.objects.live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return _('Event')

    def get_page_type(self):
        return 'event'

    def get_page_authors(self):
        # a bit dirty
        return [self.event_location]

    def time_relevance(self):
        return abs(int(now().timestamp() - int(self.date.strftime('%s'))))
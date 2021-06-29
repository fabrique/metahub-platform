from functools import reduce

from django.db.models import Q
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string

from metahub.core.models import MetaHubBasePage
from metahub.news.models import MetaHubNewsPage
from metahub.starling_metahub.organisms.blocks import OrganismActualitiesLandingHeaderRegularBlock
from metahub.starling_metahub.organisms.interfaces import OrganismCardGridRegular


class MetaHubActualitiesLandingPage(MetaHubBasePage):
    """
    This page is the landing for an overview of both events
    and news.
    """
    parent_page_types = ['home.MetaHubHomePage']

    header = StreamField([
        ('header', OrganismActualitiesLandingHeaderRegularBlock()),
    ])

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        StreamFieldPanel('header'),
    ]

    def get_all_news_and_events(self):
        # news = MetaHubNewsPage.objects.live()

        model_types = [*map(resolve_model_string, ['news.MetaHubNewsPage', 'news.MetaHubEventPage'])]
        valid_types = reduce(Q.__or__, map(Page.objects.type_q, model_types))
        news_and_events = Page.objects.filter(valid_types).specific()

        news_and_events_list = list(news_and_events)
        sorted_news_and_events = sorted(news_and_events_list, key=lambda e: e.time_relevance())
        return sorted_news_and_events

    def get_actualities_landing_grid_component(self):
        return OrganismCardGridRegular(
            title='Latest',
            cards=[p.get_card_representation() for p in self.get_all_news_and_events()]
        )



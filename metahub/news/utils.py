from functools import reduce

from django.db.models import Q
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string


def get_all_news_and_events():
    model_types = [*map(resolve_model_string, ['news.MetaHubNewsPage', 'news.MetaHubEventPage'])]
    valid_types = reduce(Q.__or__, map(Page.objects.type_q, model_types))
    news_and_events = Page.objects.filter(valid_types).specific()
    return sorted(list(news_and_events), key=lambda e: e.time_relevance())
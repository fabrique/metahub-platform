from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.utils import translation
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string

LANGUAGES = settings.LANGUAGES
LCODES = [d[0] for d in LANGUAGES]

def get_all_news_and_events(language=None):
    model_types = [*map(resolve_model_string, ['news.MetaHubNewsPage', 'news.MetaHubEventPage'])]
    valid_types = reduce(Q.__or__, map(Page.objects.type_q, model_types))
    news_and_events = Page.objects.filter(valid_types).live().specific()

    deflist = []
    for n in news_and_events:
        found = 0

        for an in n.get_ancestors():
            if an.slug in LCODES:
                if an.slug == language:
                    deflist.append(n)
                found = 1

        if not language:  #default behaviour
            if not found:
                deflist.append(n)

    return sorted(list(deflist), key=lambda e: e.time_relevance())
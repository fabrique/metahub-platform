from functools import reduce

from django.conf import settings
from django.utils.translation import ugettext_lazy as _, get_language

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from pure_pagination import Paginator
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string

from metahub.collection.models import MetaHubObjectPage
from metahub.core.models import MetaHubBasePage
from metahub.home.models import MetaHubHomePage
from metahub.locations.models import MetaHubLocationPage
from metahub.starling_metahub.organisms.interfaces import OrganismExploreSearchHeader, OrganismSearchCardGridRegular
from metahub.starling_metahub.utils import create_paginator_component
from metahub.stories.models import MetaHubStoryPage


LANGUAGES = settings.LANGUAGES
LCODES = [d[0] for d in LANGUAGES]

class MetaHubSearchPage(RoutablePageMixin, MetaHubBasePage):
    """
    Page with search header that supports live search on top, and filters below.
    Results are rendered on a card grid and refreshed using AJAX.
    """

    parent_page_types = ['home.MetahubHomePage']

    def get_search_header_component(self, applied_filters, search_query):
        # Determine if they should get active class
        # (a bit ugly but this is temporary since search will be expanded later with ES)
        all_active = len(applied_filters.items()) == 0
        story_active = applied_filters.get('type') == 'story'
        objects_active = applied_filters.get('type') == 'object'
        location_active = applied_filters.get('type') == 'location'

        active_class = 'active'

        return OrganismExploreSearchHeader(
            title=_("Explore"),
            search_button_title=_("Search"),
            search_query=search_query or '',
            placeholder_text=_("Type your query here"),
            main_filters={
                'all' : {
                    'title' : _('All'),
                    'active' : active_class if all_active else ''
                },
                'objects' : {
                    'title' : _('Objects'),
                    'querystring' : '?id_type=object',
                    'active' : active_class if objects_active else ''
                },
                'stories' : {
                    'title' : _('Stories'),
                    'querystring' : '?id_type=story',
                    'active' : active_class if story_active else ''
                },
                'locations' : {
                    'title' : _('Locations'),
                    'querystring' : '?id_type=location',
                    'active' : active_class if location_active else ''
                },
            }
        )

    def get_all_entities_in_collection_qs(self, search_query):
        model_types = [*map(resolve_model_string, ['stories.MetaHubStoryPage', 'collection.MetaHubObjectPage', 'locations.MetaHubLocationPage'])]
        valid_types = reduce(Q.__or__, map(Page.objects.type_q, model_types))
        all_entities = Page.objects.filter(valid_types).specific().live()
        if search_query:
            ids = []

            # tags filter
            for model_type in model_types:
                ids.extend(map(lambda x: x["id"], model_type.objects.filter(tags__name__in=[search_query]).values("id")))

            # body text filter
            for entity in all_entities:
                for data in entity.content.stream_data:
                    if data["type"] in ["single_richtext", "two_column_picture_richtext", "richtext_with_link"]:
                        if search_query in data["value"]["text"]:
                            ids.append(entity.id)

            # title filter OR any page that matches tags/body text filter
            all_entities = all_entities.filter(
                Q(title__icontains=search_query) | Q(id__in=ids)
            )
        return all_entities

    def get_active_filters(self, request):
        """
        Reconstructs filters according to the current situation. Since this also affects
        the available result count we use the facets from ES again.
        """
        get_vars = request.GET

        # Check this list of facet filters
        str_facets = ['artist', 'material', 'tags', 'object_category', 'provenance', 'type', 'series', 'is_highlight']
        af = {}
        for f in str_facets:
            value = get_vars.get('id_{}'.format(f))
            if value:
                af[f] = value
        return af

    def get_querystring_extras(self, applied_filters):
        """ Extra params to add to pagination so active filters are maintained. """
        extra_params = []
        for key, value in applied_filters.items():
            extra_params.append(f"&id_{key}={value}")
        return ''.join(extra_params)

    def filter_on_language(self, results):
        #take a page query list and sanitize it for language filters

        #fetch homepages and connect them to language
        hp = MetaHubHomePage.objects.live()
        language = get_language()

        include_path = None  #so by default we query all
        exclude_path = None  #by default not needed
        for p in hp:
            if p.slug in LCODES:
                if p.slug == language:
                    include_path = p.path
                else:
                    exclude_path = p.path

        if exclude_path:
            results = results.exclude(path__startswith=exclude_path)
        if include_path:
            results = results.filter(path__startswith=include_path)

        return results


    def get_search_results(self, filters, search_query):
        if filters.get('type') == 'object':
            return [p.get_card_representation() for p in self.filter_on_language(MetaHubObjectPage.objects.live())]
        elif filters.get('type') == 'story':
            return [p.get_card_representation() for p in self.filter_on_language(MetaHubStoryPage.objects.live())]
        elif filters.get('type') == 'location':
            return [p.get_card_representation() for p in self.filter_on_language(MetaHubLocationPage.objects.live())]
        return [p.get_card_representation() for p in self.filter_on_language(self.get_all_entities_in_collection_qs(search_query))]

    def create_paginator_component(self, paginator, paginator_page, querystring_extra):
        return create_paginator_component(paginator, paginator_page, querystring_extra=querystring_extra)

    def get_context(self, request, *args, **kwargs):
        context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)
        search_query = request.GET.get('q')
        applied_filters = self.get_active_filters(request)
        search_results = self.get_search_results(applied_filters, search_query)
        querystring_extra = self.get_querystring_extras(applied_filters)

        # Pagination for found objects
        MAX_ITEMS_PER_PAGE = 12
        page_number = request.GET.get('page', 1)
        paginator = Paginator(search_results, request=request, per_page=MAX_ITEMS_PER_PAGE)

        try:
            page = paginator.validate_number(page_number)
        except PageNotAnInteger:
            page = 1

        paginator_page = paginator.page(page)

        context.update({
            'results': paginator_page.object_list,
            'paginator': self.create_paginator_component(paginator, paginator_page, querystring_extra),
            'search_filters': applied_filters,
            'search_query': search_query,
            'search_header_component': self.get_search_header_component(applied_filters, search_query)
        })

        context['result_count'] = '{} Resultate'.format(len(search_results))
        return context

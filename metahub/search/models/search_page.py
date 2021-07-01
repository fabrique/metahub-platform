from functools import reduce
from random import randint

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from pure_pagination import Paginator
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.utils import resolve_model_string

from metahub.collection.models import MetaHubObjectPage
from metahub.core.models import MetaHubBasePage
# from metahub.search.search import do_search, get_search_results, get_result_as_cards, get_result_filters
from metahub.starling_metahub.organisms.interfaces import OrganismExploreSearchHeader, OrganismSearchCardGridRegular
from metahub.stories.models import MetaHubStoryPage


class MetaHubSearchPage(RoutablePageMixin, MetaHubBasePage):
    """
    Page with search header that supports live search on top, and filters below.
    Results are rendered on a card grid and refreshed using AJAX.
    """

    parent_page_types = ['home.MetahubHomePage']


    def get_search_header_component(self, applied_filters):
        # Determine if they should get active class (a bit ugly but this is temporary)
        all_active = not applied_filters.get('type') and not applied_filters.get('story')
        story_active = applied_filters.get('story')
        objects_active = applied_filters.get('objects')
        active_class = 'explore-intro__filter--active'

        return OrganismExploreSearchHeader(
            title="Explore",
            search_button_title="Search",
            main_filters={
                'all' : {
                    'title' : 'All',
                    'active' : active_class if all_active else ''
                },
                'objects' : {
                    'title' : 'Objects',
                    'querystring' : '?id_type=object',
                    'active' : active_class if objects_active else ''
                },
                'stories' : {
                    'title' : 'Stories',
                    'querystring' : '?id_type=story',
                    'active' : active_class if story_active else ''
                }
            }
        )

    def get_all_objects_and_stories_queryset(self):
        model_types = [*map(resolve_model_string, ['stories.MetaHubStoryPage', 'collection.MetaHubObjectPage'])]
        valid_types = reduce(Q.__or__, map(Page.objects.type_q, model_types))
        objects_and_stories = Page.objects.filter(valid_types).specific().live()
        return objects_and_stories

    def get_search_card_grid_component(self):
        return OrganismSearchCardGridRegular(
            cards=[p.get_card_representation() for p in self.get_all_objects_and_stories_queryset()]
        )

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

    def get_search_results(self, filters):
        if filters.get('type') == 'object':
            return [p.get_card_representation for p in MetaHubObjectPage.objects.live()]
        if filters.get('type') == 'story':
            return [p.get_card_representation for p in MetaHubStoryPage.objects.live()]
        return [p.get_card_representation() for p in self.get_all_objects_and_stories_queryset()]

    def get_context(self, request, *args, **kwargs):
        context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)
        search_string = request.GET.get('search')
        applied_filters = self.get_active_filters(request)
        search_results = self.get_search_results(applied_filters)


        # Pagination for found objects
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(search_results, request=request, per_page=12)
        paginator_page = paginator.page(page)

        context.update({
            'results': paginator_page.object_list,
            'paginator': paginator_page,
            'search_filters' : applied_filters,
            'search_query' : search_string,
            'search_header_component' : self.get_search_header_component(applied_filters)
        })

        context['result_count'] = '{} Resultate'.format(len(search_results))
        return context

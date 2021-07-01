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


    def get_search_header_component(self):
        return OrganismExploreSearchHeader(
            title="Explore",
            search_button_title="Search"
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

    # def search_view(self, request, *args, **kwargs):
    #     """
    #     Used by the AJAX request done on the search landing so that not all
    #     the page refreshes but only the results/cards at the bottom.
    #     """
    #     context = self.get_context(request, *args, **kwargs)
    #     content = render_to_string('core/components/search_filter_results.html', context=context)
    #     output = {}
    #     output['content'] = content
    #     return JsonResponse(data=output, safe=False)
    #
    # def live_search_url(self):
    #     return self.url + self.reverse_subpage('livesearch_landing')
    #
    # def search_url(self):
    #     return self.url + self.reverse_subpage('regular_landing')
    #
    # @route(r'^live/')
    # def livesearch_landing(self, request, *args, **kwargs):
    #     """
    #     Used to determine and render the livesearch results. Stringifies the template
    #     so frontend can render it as is immediately.
    #     """
    #
    #     # Required to avoid circular imports
    #
    #
    #     query = request.GET.get('search')
    #     context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)
    #
    #     # Get first 5 results and output the template for the livesearch bar
    #     context['results'] = do_search(query)[:5]
    #     content = render_to_string('core/components/search_bar_result.html', context=context)
    #     output = {}
    #     output['content'] = content
    #     return JsonResponse(data=output, safe=False)
    #
    # @route(r'^$')
    # def regular_landing(self, request, *args, **kwargs):
    #     """
    #     Landing with header on top and search results at the bottom. Initially
    #     loads all results if no params are given, subsequent search operations
    #     are handled by AJAX.
    #     """
    #     if request.is_ajax():
    #         return self.search_view(request, *args, **kwargs)
    #
    #     return Page.serve(self, request, *args, **kwargs)
    #
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
        if filters['id_type'] == 'object':
            return [p.get_card_representation for p in MetaHubObjectPage.objects.live()]
        if filters['id_type'] == 'story':
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
            'search_query' : search_string
        })

        context['result_count'] = '{} Resultate'.format(len(search_results))
        return context

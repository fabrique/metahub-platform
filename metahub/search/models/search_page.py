from random import randint

from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from pure_pagination import Paginator
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from metahub.core.models import MetaHubBasePage
from metahub.search.search import do_search, get_search_results, get_result_as_cards, get_result_filters


class MetaHubSearchPage(RoutablePageMixin, MetaHubBasePage):
    """
    Page with search header that supports live search on top, and filters below.
    Results are rendered on a card grid and refreshed using AJAX.
    """

    parent_page_types = ['home.MetahubHomePage']

    # search_header = StreamField([
    #     ('search_header', OrganismSearchHeaderRegularBlock())
    # ])
    #
    # content_panels = MetahubBasePage.content_panels + [
    #     StreamFieldPanel('search_header'),
    # ]
    #
    # def get_random_header_picture(self):
    #     """
    #     Picks one of the chosen header images.
    #     """
    #     try:
    #         header_child = self.search_header[0]
    #     except IndexError:
    #         return None
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         picture_index = randint(0, len(picture_structvalues) - 1)
    #         return picture_index
    #
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
    # def get_active_filters(self, request):
    #     """
    #     Reconstructs filters according to the current situation. Since this also affects
    #     the available result count we use the facets from ES again.
    #     """
    #     get_vars = request.GET
    #
    #     # Check this list of facet filters
    #     str_facets = ['artist', 'material', 'tags', 'object_category', 'provenance', 'type', 'series', 'is_highlight']
    #     af = {}
    #     for f in str_facets:
    #         value = get_vars.get('id_{}'.format(f))
    #         if value:
    #             af[f] = value
    #
    #     # We need to reconstruct the date object, actually no, since we do a range query by hand
    #     # TODO: Does urllib.parse need a safety try/catch?
    #     # date_facets = ['dating_from', 'dating_to']
    #     # for f in date_facets:
    #     #     value = get_vars.get('id_{}'.format(f))
    #     #
    #     #     if value:
    #     #         date_str = urllib.parse.unquote(value)
    #     #         date_str = "{}-1-1".format(date_str)
    #     #         try:
    #     #             date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    #     #         except ValueError:
    #     #             pass # Date was not in right format in url, skip it
    #     #         else:
    #     #             af[f] = date_obj
    #     return af
    #
    # def get_context(self, request, *args, **kwargs):
    #
    #     context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)
    #     search_string = request.GET.get('search')
    #     applied_filters = self.get_active_filters(request)
    #     search_results = get_search_results(search_string, applied_filters, request.GET)
    #
    #     # Try to parse the results, if there are none use highlights
    #     search_results_cards = get_result_as_cards(search_results)
    #
    #     if len(search_results_cards) == 0:
    #         search_results_cards = self.get_highlights()
    #         context['no_results'] = True
    #
    #     context['filters'] = get_result_filters(search_results, request.GET)
    #
    #     # Pagination for found objects
    #     try:
    #         page = request.GET.get('page', 1)
    #     except PageNotAnInteger:
    #         page = 1
    #
    #     paginator = Paginator(search_results_cards, request=request, per_page=12)
    #     paginator_page = paginator.page(page)
    #
    #     context.update({
    #         'results': paginator_page.object_list,
    #         'paginator': paginator_page,
    #         'search_filters' : applied_filters,
    #         'search_query' : search_string
    #     })
    #
    #     context['result_count'] = '{} Resultate'.format(len(search_results))
    #     return context

# from datetime import timedelta, datetime
#
# from django.conf import settings
# from django_elasticsearch_dsl import Index
# # from elasticsearch_dsl import iteritems # this does not exist anymore?
# from elasticsearch_dsl.faceted_search import Facet
# from elasticsearch_dsl.query import Q, Range
#
# from elasticsearch_dsl import FacetedSearch, TermsFacet
#
# from metahub.starling_metahub.atoms.interfaces import AtomDropdownFilterRegular, AtomDropdownOption
# from metahub.starling_metahub.molecules.interfaces import MoleculeObjectCardRegular, MoleculeContextCardRegular
#
#
# class ObjectSearch(FacetedSearch):
#     """
#     Searches through objects (which can be part of objectseries) and story pages.
#     Also builds the facets which are responsible for the filtering options
#     on the search page.
#     """
#
#     # Circular import circumvention
#     from metahub.search.documents import CollectionObjectDocument
#     from metahub.search.documents import StoryDocument
#     doc_types = [CollectionObjectDocument, StoryDocument]
#     index = settings.ES_INDEX_NAME  #important, otherwise it queries all indices...
#
#     # Fields that should be searched  # MKR this does not seem to work since we query manually
#     fields = ['artist',
#               # 'title',
#               # 'description',
#               # 'material',
#               # 'tags',
#               # 'object_category',
#               # 'type',
#               # 'highlight_intro',
#               # 'datings',
#               # 'dating_from_df',
#               # 'dating_to_df',
#               # 'tag_synonyms',
#               ]
#
#     facets = {
#         # Use bucket aggregations to define facets, 10 is default but 100 should be enough
#         'artist': TermsFacet(field='artist', size=1000),
#         'material': TermsFacet(field='material', size=1000),
#         'object_category' : TermsFacet(field='object_category', size=1000),
#         'provenance' : TermsFacet(field='provenance', size=1000),
#         'type' : TermsFacet(field='type', size=1000),
#         # 'dating_from' : DateHistogramFacet(field='dating_from_df', interval='year'),
#         # 'dating_to' : DateHistogramFacet(field='dating_to_df', interval='year'),
#         'is_highlight' : TermsFacet(field='is_highlight', size=2),
#         'series': TermsFacet(field='series_id', size=1000),
#         'tags': TermsFacet(field='tags', size=5000),
#     }
#
#     def __init__(self, query=None, filters={}, sort=(), getvars={}):
#         """
#         :arg query: the text to search for
#         :arg filters: facet values to filter
#         :arg sort: sort information to be passed to :class:`~elasticsearch_dsl.Search`
#         """
#         print("Query: ", query)
#
#         self._query = query
#         self._filters = {}
#         self._sort = sort
#         self.filter_values = {}
#         self.facet_filters = filters
#         #date variables for range search
#         self.getvars = getvars
#
#         # for name, value in iteritems(filters):
#         for name, value in filters:
#             self.add_filter(name, value)
#         self._s = self.build_search()
#
#     def search(self):
#         """
#         Override search to add your own filters.
#         """
#
#         s = super(ObjectSearch, self).search()
#
#         # for k,v in self.facet_filters.items(): #// TODO make this dynamic // MKR not sure why this is needed, i thought for total results number but it seems to work?
#         #     if k =='material':
#         #         s = s.filter('term', material=v)
#
#         if self.getvars.get('id_dating_from'):
#             fromdate = int(self.getvars.get('id_dating_from', 0))  # parse to int. just being careful
#             s = s.filter('range', dating_from_df={'gt': fromdate, 'lte': 3000})
#         if self.getvars.get('id_dating_to'):
#             todate = int(self.getvars.get('id_dating_to', 0))  # parse to int. just being careful
#             s = s.filter('range', dating_to_df={'gt': 1000, 'lte': todate})
#
#         return s
#
#     def query(self, search, query):
#
#         searchterm = self._query
#         if not searchterm:
#             return search
#
#         # fields is not supported for match_phrase or match_phrase_prefix, so we define it manually
#         # see also https://github.com/elastic/elasticsearch-dsl-py/issues/925
#         # we can use  this for livesearch , searches for results starting with the searchterm (up to a certain amount of expansions) which can be adjusted
#         # https://www.elastic.co/guide/en/elasticsearch/reference/6.4/query-dsl-match-query-phrase-prefix.html
#         q = Q('bool',
#               should=[
#                   Q("match_phrase_prefix", title=searchterm),
#                       Q("match_phrase_prefix", artist_ls=searchterm),
#                       Q("match_phrase_prefix", tags_ls=searchterm),
#                       Q("match_phrase_prefix", tag_synonyms=searchterm),
#                       Q("match_phrase_prefix", material_ls=searchterm),
#                       Q("match_phrase_prefix", description=searchterm),
#                       Q("match_phrase_prefix", highlight_intro=searchterm),
#                       Q("match_phrase_prefix", type=searchterm)],
#               minimum_should_match=1
#               )
#         return search.query(q)
#
# def get_all():
#     """
#     Gets all objects and stories.
#     """
#     i = Index(settings.ES_INDEX_NAME)
#     search = ObjectSearch()
#     total = search.count()
#     search = search[0:total]
#     # search = search[0:15] ## temporary
#     results = search.execute()
#     return results
#
#
# def get_result_filters(response, getvars={}):
#     """
#     This sets up filter interfaces for use in the template
#     all based on ES facets of course.
#     """
#
#     filters = []
#
#     artistfacets = []
#     response.facets.artist.sort(key=lambda x:x[0])
#     for (facet, count, selected) in response.facets.artist:
#         if facet != '':
#             artistfacets.append(
#                 AtomDropdownOption(
#                     value=facet,
#                     title='{} ({})'.format(facet,count)
#                 )
#             )
#
#     themefacets = []
#     response.facets.type.sort(key=lambda x:x[0])
#     for (facet, count, selected) in response.facets.type:  #only story and object, so probably merge with object_type ?
#         themefacets.append(
#             AtomDropdownOption(
#                 value=facet,
#                 title='{} ({})'.format(facet,count)
#             )
#         )
#
#     materialfacets = []
#     response.facets.material.sort(key=lambda x:x[0])
#     for (facet, count, selected) in response.facets.material:
#         if facet != '':
#             materialfacets.append(
#                 AtomDropdownOption(
#                     value=facet,
#                     title='{} ({})'.format(facet,count)
#                 )
#             )
#
#     categoryfacets = []
#     response.facets.object_category.sort(key=lambda x:x[0])
#     for (facet, count, selected) in response.facets.object_category:
#         if facet != '':
#             categoryfacets.append(
#                 AtomDropdownOption(
#                     value=facet,
#                     title='{} ({})'.format(facet,count)
#                 )
#             )
#
#     provenancefacets = []
#     response.facets.provenance.sort(key=lambda x:x[0])
#     for (facet, count, selected) in response.facets.provenance:
#         if facet != '':
#             provenancefacets.append(
#                 AtomDropdownOption(
#                     value=facet,
#                     title='{} ({})'.format(facet,count)
#                 )
#             )
#
#     dating_fromfacets = []
#     # print('datefrom facets:', response.facets.dating_from)
#     # for (facet, count, selected) in response.facets.dating_from:
#     #     print(facet.year, count)
#         # dating_fromfacets.append(
#         #     AtomDropdownOption(
#         #         value=facet.year,
#         #         title='{} ({})'.format(facet.year,count)
#         #     )
#         # )
#     #
#     # dating_tofacets = []
#     # for (facet, count, selected) in response.facets.dating_to:
#     #     dating_tofacets.append(
#     #         AtomDropdownOption(
#     #             value=facet.year,
#     #             title='{} ({})'.format(facet.year,count)
#     #         )
#     #     )
#
#     date_from = getvars.get('id_dating_from','')  #this is nasty, but it works for now
#     date_to = getvars.get('id_dating_to','')
#     yearranges = [i for i in range(1000,2000,100)]
#     facetfilter = AtomDropdownFilterRegular(
#         name='dating_from',
#         placeholder='Datierung',
#         type='date',
#         options=[date_from,date_to] + yearranges
#     )
#
#     filters.append(facetfilter)
#
#     facetfilter = AtomDropdownFilterRegular(
#         name='artist',
#         placeholder='Künstler*in',
#         options=artistfacets
#     )
#     filters.append(facetfilter)
#
#     # disable for now
#     # facetfilter = AtomDropdownFilterRegular(
#     #     name='provenance',
#     #     placeholder='Vorbesitz',
#     #     options=provenancefacets
#     # )
#     # filters.append(facetfilter)
#
#     facetfilter = AtomDropdownFilterRegular(
#         name='object_category',
#         placeholder='Objektbezeichnung',
#         options=categoryfacets
#     )
#     filters.append(facetfilter)
#
#     facetfilter = AtomDropdownFilterRegular(
#         name='type',
#         placeholder='Kategorie',
#         options=themefacets
#     )
#     filters.append(facetfilter)
#
#     # facetfilter = AtomDropdownFilterRegular(
#     #     name='material',
#     #     placeholder='Material & Technik',
#     #     options=materialfacets
#     # )
#     # filters.append(facetfilter)
#
#
#     # facetfilter = AtomDropdownFilterRegular(
#     #     name='dating_to',
#     #     placeholder='Datierung Bis',
#     #     options=dating_tofacets
#     # )
#     # filters.append(facetfilter)
#
#     return filters
#
#
# def get_search_results(term, filters, getvars={}):
#     """
#     This gets search results, and applies filters
#     to be used when creating cards, filters etc.
#     """
#     if term or filters or getvars:
#         response = do_search(term, filters, getvars)
#     else:
#         response = get_all()
#     return response
#
# def get_result_as_cards(response):
#     """
#     Builds the cards for the search result, both documents define the get method.
#     Returns the right data for the frontend to render.
#     """
#     cards = []
#     for hit in response:
#         if hit.result_type == 'story':
#             cards.append(MoleculeContextCardRegular(
#                     href=hit.url,
#                     title=hit.title,
#                     type=hit.type,
#                     color='blurple',
#                     picture={
#                         'images': {'mobile': hit.primary_image},
#                         'positions': {'mobile': '50% 50%'},
#                         'fits': {'mobile': 'cover'},
#                         'width': 1920,
#                         'height': 640
#                     }
#                 ))
#
#         if hit.result_type == 'object':
#             cards.append(MoleculeObjectCardRegular(
#                     href=hit.url,
#                     title=hit.title,
#                     name=hit.artist,
#                     type=hit.object_type,
#                     date=hit.datings,
#                     picture={
#                         'images': {'mobile': hit.primary_image},
#                         'positions': {'mobile': '50% 50%'},
#                         'fits': {'mobile': 'cover'},
#                         'width': 1920,
#                         'height': 640
#                     }
#                 ))
#     return cards
#
#
# def do_search(q, filters={}, getvars={}):
#     # clear for now
#     i = Index(settings.ES_INDEX_NAME)
#     i.clear_cache()
#     bs = ObjectSearch(q, filters=filters, getvars=getvars)
#
#     total = bs.count()
#     bs = bs[0:total]
#
#     response = bs.execute()
#
#     # for debugging print hits and other attributes as usual
#     # total = response.hits.total
#     # print('total hits!!', total)
#     # for hit in response:
#     #     print(hit.meta.score, hit.title, hit.material, hit.artist)
#     #
#     # for (facet, count, selected) in response.facets.artist:
#     #     print('Artist: {} {} '.format(facet, count))
#     # #
#     # for (facet, count, selected) in response.facets.material:
#     #     # print(selected)
#     #     # if selected:
#     #     print('Material: {} {} '.format(facet, count))
#     #
#     # for (facet, count, selected) in response.facets.beecollect_tags:
#     #     print('Tag: {} {} '.format(facet, count))
#     #
#     # for (facet, count, selected) in response.facets.object_category:
#     #     print('Category: {} {} '.format(facet, count))
#     #
#     # for (facet, count, selected) in response.facets.provenance:
#     #     print('provenance: {} {} '.format(facet, count))
#
#
#     return response
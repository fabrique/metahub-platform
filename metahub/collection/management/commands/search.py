from django_elasticsearch_dsl import Index
from elasticsearch_dsl import FacetedSearch, iteritems
from elasticsearch_dsl.query import MultiMatch

from metahub.collection.documents import CollectionObjectDocument

from django.core.management import BaseCommand

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from django.conf import settings
from ...search import ObjectSearch

#https://iridakos.com/programming/2018/10/22/elasticsearch-bucket-aggregations
#First you add a filter, then you define the aggregations and finally you execute your search.

class Command(BaseCommand):
    help = 'Imports the json with beecollect data from the specified path'

    def handle(self, *args, **options):
        #cars = CarDocument.search().query("match", model_name=q)

        ## TODO wildcard or fuzzy search for words
        ## suggestions for typos :https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#suggestions
        ## highlights: https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#highlighting

        #clear for now
        i = Index(settings.ES_INDEX_NAME)
        i.clear_cache()

        q = 'deckel'
        material = 'Aluminium'  # has 2 results atm
        filters = {'material': material}
        filters = {}
        # filters = {"artist": "Dan Givon"}
        bs = ObjectSearch(q, filters=filters)
        # bs = ObjectSearch(filters={"artist": "Dan Givon"})  #strangely enough this does not aggregate the filtered facets so do it in the class instead...
        response = bs.execute()

        # access hits and other attributes as usual
        total = response.hits.total
        print('total hits', total)

        for hit in response:
            print("score: {} [] {} [] material: {}".format(hit.meta.score, hit.title, hit.material))

        # for (facet, count, selected) in response.facets.artist:
        #     print('Artist: {} {} '.format(facet,count))
        #
        # for (facet, count, selected) in response.facets.material:
            # print(selected)
            # if selected:
            # print('material: {} {} '.format(facet,count))

        for (facet, count, selected) in response.facets.beecollect_tags:
            print('Tag: {} {} '.format(facet, count))

        for (facet, count, selected) in response.facets.object_category:
            print('Category: {} {} '.format(facet, count))

        return 'done'

        query1 = MultiMatch(query=q,  fields=['title','description','artist'],fuzziness='AUTO')

        s = CollectionObjectDocument.search().query(query1)
        total = s.count()
        s= s[0:total]
        cars = s.execute()
        print('results: {}'.format(total))
        for hit in cars:
            print(
                "object name : {}, description {} - otype {} - artist {}".format(hit.title,hit.description, hit.object_type, hit.artist)
            )

        # paginator = Paginator(cars, 100)
        # page = request.GET.get('page')
        # cars = paginator.get_page(page)


       # return render(request, 'search/search.html', {'cars': cars})

    # FacetedSearch
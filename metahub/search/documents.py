from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from metahub.collection.models import BaseCollectionObject
from metahub.stories.models import MetaHubStoryPage


@registry.register_document
class StoryDocument(Document):

    def get_queryset(self):
        return self.django.model.objects.live()

    class Index:
        # Name of the Elasticsearch index, See Elasticsearch Indices API reference for avaßilable settings
        name = settings.ES_INDEX_NAME
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    # Object data necessary to create clickable card
    # url = fields.TextField(attr="url")
    # type = fields.KeywordField(attr="get_category")
    # primary_image = fields.TextField(attr="get_elasticsearch_image")
    # is_highlight = fields.KeywordField(attr="is_highlight")
    # tags = fields.KeywordField(attr="get_tags_as_list")  #for now always empty
    # tags_ls = fields.TextField(attr="get_tags_as_list")  # they will probably add tags with capitals so yea..
    #
    # artist = fields.KeywordField()
    # material = fields.KeywordField()
    # object_category = fields.KeywordField()
    # provenance = fields.KeywordField()
    # series_id = fields.KeywordField()
    # result_type = fields.TextField()

    # def prepare_result_type(self, instance):
    #     return 'story'
    #
    # def prepare_artist(self, instance):
    #     return ''  # stubs otherwise faceting breaks stuff
    #
    # def prepare_material(self, instance):
    #     return ''
    #
    # def prepare_object_category(self, instance):
    #     return ''  # stubs otherwise faceting breaks stuff
    #
    # def prepare_provenance(self, instance):
    #     return ''
    #
    # def prepare_series_id(self, instance):
    #     return ''

    class Django:
        model = MetaHubStoryPage

        # # The fields of the model you want to be indexed in Elasticsearch
        # fields = [
        #     'title',
        #     'highlight_intro',
        # ]



@registry.register_document
class CollectionObjectDocument(Document):

    def get_queryset(self):
        return self.django.model.objects.all().filter(associated_page__live=True)

    class Index:
        # Name of the Elasticsearch index
        name = settings.ES_INDEX_NAME
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    material = fields.KeywordField(attr="material")
    material_ls = fields.TextField(attr="material")
    tags = fields.KeywordField(attr="get_object_page_tags")
    tags_ls = fields.TextField(attr="get_object_page_tags")  # they will probably add tags with capitals so yea..
    object_category = fields.KeywordField(attr="object_type")
    artist = fields.KeywordField(attr="artist_to_string") # for facetting
    artist_ls = fields.TextField(attr="artist_to_string")  # MKR for (live)search, case insensitive
    primary_image = fields.KeywordField(attr="get_elasticsearch_image")
    provenance = fields.KeywordField(attr="provenance")
    url = fields.TextField(attr="get_object_page_url")
    series_id = fields.KeywordField(attr="get_series_page_id")
    is_highlight = fields.KeywordField(attr="get_is_highlight")
    type = fields.KeywordField(attr="get_object_type")
    result_type = fields.TextField()

    def prepare_result_type(self, instance):
        return 'object'

    class Django:
        model = BaseCollectionObject

        # The fields of the model you want to be indexed in Elasticsearch
        # note these are all case insensitive indexed ;)
        fields = [
            'title',
            'description',
            'object_type',
            'bc_inventory_number',
            'datings',
            'dating_from_df',
            'dating_to_df',
            'tag_synonyms'
        ]
from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from starling.utils import render, if2context

from .models import BaseCollectionObject
from ..starling_metahub.molecules.interfaces import MoleculeObjectCardRegular


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

from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from starling.interfaces.molecules import MoleculeCardRegular
from starling.utils import render, if2context

from metahub.starling_metahub.molecules.interfaces import MoleculeObjectCardRegular, MoleculeContextCardRegular


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
    url = fields.TextField(attr="url")
    type = fields.KeywordField(attr="get_category")
    primary_image = fields.TextField(attr="get_elasticsearch_image")
    is_highlight = fields.KeywordField(attr="is_highlight")
    tags = fields.KeywordField(attr="get_tags_as_list")  #for now always empty
    tags_ls = fields.TextField(attr="get_tags_as_list")  # they will probably add tags with capitals so yea..

    artist = fields.KeywordField()
    material = fields.KeywordField()
    object_category = fields.KeywordField()
    provenance = fields.KeywordField()
    series_id = fields.KeywordField()
    result_type = fields.TextField()

    def prepare_result_type(self, instance):
        return 'story'

    def prepare_artist(self, instance):
        return ''  # stubs otherwise faceting breaks stuff

    def prepare_material(self, instance):
        return ''

    def prepare_object_category(self, instance):
        return ''  # stubs otherwise faceting breaks stuff

    def prepare_provenance(self, instance):
        return ''

    def prepare_series_id(self, instance):
        return ''

    class Django:
        from metahub.core.models import MetaHubStoryPage
        model = MetaHubStoryPage

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'highlight_intro',
        ]

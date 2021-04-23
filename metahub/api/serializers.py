from rest_framework import serializers
from wagtail.core.models import Site
from wagtail.images.api.fields import ImageRenditionField

from metahub.collection.models import BaseCollectionObject
from metahub.core.models import MetaHubStoryPage


class StoryPageSerializer(serializers.ModelSerializer):
    domain = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    class Meta:
        model = MetaHubStoryPage
        fields = ('rest_api_id',
                  'domain',
                  'url',
                  'title',
                  'abstract',
                  'label',
                  'image')

    def get_domain(self, obj):
        return Site.objects.get(is_default_site=True).root_url

    def get_label(self, obj):
        """
        Gets page type/category (Geschischten, Objekt, etc)
        """
        try:
            return str(obj.collection_category)
        except AttributeError:
            return 'Unbekannt'

    def get_abstract(self, obj):
        return obj.highlight_intro

    def get_image(self, obj):
        image = obj.get_api_compatible_image()
        # return ''
        return ImageRenditionField('fill-100x200').to_representation(image)


class BaseCollectionObjectSerializer(serializers.ModelSerializer):
    domain = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = BaseCollectionObject
        fields = ('bc_inventory_number',
                  'domain',
                  'title',
                  'artist',
                  'image',
                  'url',
                  'label',
                  'type',
                  'abstract',
                  'tags',
                  'year')

    def get_domain(self, obj):
        return Site.objects.get(is_default_site=True).root_url

    def get_type(self, obj):
        return obj.object_type

    def get_label(self, obj):
        """
        Gets page type/category (Geschischten, Objekt, etc)
        """
        page = obj.associated_page.first()
        if page:
            return str(page.collection_category)
        else:
            return 'Unbekannt'

    def get_abstract(self, obj):
        """
        Short intro text.
        """
        page = obj.associated_page.first()
        if page:
            return page.highlight_intro
        else:
            return ''

    def get_tags(self, obj):
        page = obj.associated_page.first()
        if page:
            return page.get_api_tags()
        else:
            return []

    def get_url(self, obj):
        """
        Gets Wagtail Page url for object if it exists.
        TODO: Return 404 page directly if objectpage not found?
        """
        page = obj.associated_page.first()
        if page:
            return page.url
        else:
            return 'reverse relative 404?'

    def get_image(self, obj):
        """
        Uses primary image to construct various sizes used by Fork.
        """
        images = obj.obj_img_link.all()
        if images:
            image = images.first().object_image
            return {
                '320w-16x10' : ImageRenditionField('fill-320x200').to_representation(image),
                '475w-16x10': ImageRenditionField('fill-475x297').to_representation(image),
                '950w-16x10': ImageRenditionField('fill-950x594').to_representation(image),
                '350w': ImageRenditionField('width-350').to_representation(image),
                '550w': ImageRenditionField('width-550').to_representation(image),
                '750w': ImageRenditionField('width-759').to_representation(image),
                '550h': ImageRenditionField('height-550').to_representation(image),
                '1000w-1x1': ImageRenditionField('fill-1000x1000').to_representation(image),
                '1100h': ImageRenditionField('width-550').to_representation(image),
                'alt' : image.alt_text,
                'attribution' : image.attribution,
            }
        return None

    def get_year(self, obj):
        return obj.datings




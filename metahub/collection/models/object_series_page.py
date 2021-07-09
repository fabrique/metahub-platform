from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField

from metahub.collection.models import CollectionObjectSeriesTag
from metahub.core.models import MetaHubBasePage


class MetaHubObjectSeriesPage(MetaHubBasePage):
    """
    Page that represents a series of objects. Objects can be defined to belong to one
    series at a time. For some objects this is done automatically upon import from
    BeeCollect. Just like with the MetaHubObjectPage users can add rich content.

    This class overrides a lot of the methods from MetaHubBasePage. See the
    superclass for an overview of possible overrides.
    """
    parent_page_types = []

    # In case the series is defined through BeeCollect
    series_id = models.CharField(max_length=256, default=None, blank=True, null=True)

    # Amount of objects shown in the grid before "show more" appears
    MAX_SHOWN_OBJECTS = 6

    # CMS panels
    content = StreamField([
        # ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        # ('single_video', OrganismContentSingleVideoRegularBlock()),
        # ('single_image', OrganismContentSingleImageRegularBlock()),
        # ('single_audio', OrganismContentSingleAudioRegularBlock()),
        # ('double_quote_richtext', OrganismContentDoubleQuoteRichTextRegularBlock()),
        # ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        # ('objects_choice', OrganismObjectMosaicChoiceRegularBlock())
    ], blank=True)
    tags = ClusterTaggableManager(through=CollectionObjectSeriesTag, blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('tags')
    ]

    # def build_hero_header(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Creates an image based hero header automatically (cannot be set in CMS) based
    #     on the first image of every object in the series.
    #     """
    #     return OrganismHeroHeaderMultiImageRegular(
    #         information=self.get_hero_info(),
    #         expandable=True,
    #         pictures=self.get_object_images(),
    #         theme='white'
    #     )
    #
    # def get_lightbox_items(self):
    #     """
    #     Get lightbox items and information. Since we need access to the properties
    #     of the MetaHubImage object we can't reuse get_object_images for this.
    #     """
    #     data = []
    #     for object in self.get_associated_objects():
    #        image_links = object.obj_img_link.all()
    #        for image_link in image_links:
    #            image = image_link.object_image
    #            image_data = {
    #                'picture' : AtomPictureRegular(**Resolution(mobile='2048', landscape='4096', crop=True).resolve(image)),
    #                'information': {
    #                    'title' : self.title,
    #                    'name' : self.get_object_artist(),
    #                    'description': '',
    #                    'credits': image.attribution,
    #                }
    #            }
    #            data.append(image_data)
    #     return data
    #
    #
    # def get_hero_images(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     For this kind of page, images are not chosen in the CMS but are automatically
    #     retrieved from the corresponding object.
    #     """
    #     return self.get_object_images()
    #
    # def get_hero_info(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Determines information that is displayed in this page type's hero header.
    #     """
    #     return {
    #         'name': self.get_category(),
    #         'title': self.title,
    #     }
    #
    # def get_tags(self):
    #     """
    #     Generates the frontend-compatible list of tags. These are the tags from the
    #     django-taggit model, and can be managed in the CMS.
    #     """
    #     if self.tags and len(self.tags.all()) > 0:
    #         searchpage = self.get_search_base_url()
    #         tags = {'title': 'Schlagworte', 'tag_items': [{'title': str(tag), 'href': '{}?id_tags={}'.format(searchpage, str(tag)) } for tag in self.tags.all()]}
    #         return tags
    #     return None
    #
    # def get_api_tags(self):
    #     """
    #     Generates the API-compatible list of tags. These are the tags from the
    #     django-taggit model, and can be managed in the CMS.
    #     """
    #     if self.tags and len(self.tags.all()) > 0:
    #         tags = [{'title': str(tag), 'href': '/search?id_tags={}'.format(str(tag)) } for tag in self.tags.all()]
    #         return tags
    #     return []
    #
    # def get_tags_as_list(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Used for ES indexing. At the moment stories do not have tags, but
    #     this might be added in the future.
    #     """
    #     return [str(tag) for tag in self.tags.all()]
    #
    # def get_search_representation(self):
    #     """
    #     Renders card for search result views.
    #     """
    #     return self.get_object_card_representation()
    #
    # def get_card_representation(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Decides what info to present on the "Discover collection in context" card.
    #     This card format also exist for stories, in a different color.
    #     """
    #     return MoleculeContextCardRegular(
    #         href=self.url,
    #         color='white',
    #         title=self.get_hero_info()['title'],
    #         type=self.get_category(),
    #         picture=self.get_primary_image()
    #     )
    #
    # def get_object_card_representation(self, classes=''):
    #     """
    #     Object specific card representation, for example for the "related" objects
    #     component. Search results are based on this template as well but not called from
    #     here but based on indexed data.
    #     """
    #     return MoleculeObjectCardRegular(
    #         href=self.url,
    #         title=self.get_hero_info()['title'],
    #         name=self.get_hero_info()['name'],
    #         picture=self.get_primary_image(),
    #         type=self.get_category(),
    #         classes=classes
    #     )
    #
    # def get_primary_image(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Image that is used if representing the object in a card or other component.
    #     TODO: return a default image if not found (objects without image can exist)
    #     """
    #     images = self.get_object_images()
    #     if images:
    #         return images[0]
    #     else:
    #         return None
    #
    # def get_raw_images(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Used when we need the raw images and not the atomized variant.
    #     """
    #     images = []
    #     for object in self.get_associated_objects():
    #        image_links = object.obj_img_link.all()
    #        for link in image_links:
    #            images.append(link.object_image)
    #     return images
    #
    # def get_primary_object(self):
    #     objects = self.get_associated_objects()
    #     try:
    #         return objects[0]
    #     except IndexError:
    #         return None
    #
    # def get_series_objects_as_cards(self):
    #     """
    #     Returns a list of clickable cards representing each object that is
    #     part of this series.
    #     """
    #     cards = []
    #     for o in self.get_associated_objects():
    #         try:
    #             page = MetaHubObjectPage.objects.get(object=o)
    #         except MetaHubObjectPage.DoesNotExist:
    #             pass
    #         else:
    #             cards.append(page.get_object_card_representation())
    #     return cards[:self.MAX_SHOWN_OBJECTS]
    #
    # def get_series_size(self):
    #     return len(self.get_associated_objects())
    #
    # def get_series_remaining_count(self):
    #     """
    #     Calculates the amount of elements that also belong to this series but
    #     are not shown yet in the grid.
    #     TODO: Localization support
    #     """
    #     total = self.get_series_size()
    #     if total <= self.MAX_SHOWN_OBJECTS:
    #         return None
    #     else:
    #         return 'Weitere Objekte dieser Serie ({})'.format(total - self.MAX_SHOWN_OBJECTS)
    #
    # def get_series_total_string(self):
    #     """
    #     Frontend formatted text for total count.
    #     """
    #     return 'Alle Objekte ({})'.format(self.get_series_size())
    #
    # def get_elasticsearch_series_id(self):
    #     """
    #     Used to generate prefiltered search results based on a series page
    #     and its objects. Since users can make series themselves we do this
    #     on page basis, not on series_id field since this is from BeeCollect.
    #     """
    #     try:
    #         return "object_series_{}".format(self.pk)
    #     except AttributeError:
    #         return None
    #
    # def get_all_objects_url(self):
    #     """
    #     Builds the url to prefiltered search page that will show all objects
    #     that belong to this series.
    #     Example: http://localhost:6767/search/?id_series=object_series_8252
    #     """
    #     return "{}?id_series={}".format(self.get_search_base_url(), self.get_elasticsearch_series_id())
    #
    # def get_object_images(self):
    #    """
    #    For each object that belongs to the series, retrieve its first image. These
    #    images are then shown on the series page and used in the header/lightbox.
    #    """
    #    image_list = []
    #    for object in self.get_associated_objects():
    #        images = object.obj_img_link.all()
    #        image_list += [AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image.object_image)) for image in
    #                 images]
    #    return image_list
    #
    # def get_object_artist(self):
    #     """
    #     Artist of the first object, we will treat this as the main artist.
    #     """
    #     object = self.get_primary_object()
    #     if object:
    #         if object.artist:
    #             return str(object.artist)
    #     return 'Unbekannt'
    #
    # def get_associated_objects(self):
    #     """
    #     Through the foreign relation, retrieve objects that belong to this series.
    #     An object can only belong to one series at a time.
    #     """
    #     return self.collection_objects.all()
    #
    # def build_metadata(self):
    #     """
    #     Create frontend-ready data for the metadata block.
    #     Series has no metadata block at the moment.
    #     """
    #     return []
    #
    # def get_favourite_info(self):
    #     """
    #     Specifies category and unique idenfifier for this page.
    #     """
    #     return {
    #         'category' : 'series',
    #         'id': self.pk
    #     }
    #
    # def save(self, *args, **kwargs):
    #     super().save(**kwargs)
    #
    #     # If saving for the first time after creation,
    #     # add tags from the BeeCollect object to django-taggit
    #     if self.pk:
    #         if len(self.tags.all()) == 0:
    #             all_tags = []
    #             for object in self.get_associated_objects():
    #                 all_tags + object.get_bc_tags_as_list()
    #             self.tags.set(*all_tags)
    #         super().save(**kwargs)
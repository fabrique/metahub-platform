from django.db import models
from starling.interfaces.atoms import AtomPictureRegular
from starling.interfaces.generic import Resolution
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.api.fields import ImageRenditionField

from metahub.core.models import AbstractMetaHubRichBasePage
from metahub.core.utils import ReadOnlyPanel
from metahub.starling_metahub.molecules.interfaces import MoleculeContextCardRegular
from metahub.starling_metahub.organisms.blocks import OrganismHeroHeaderMultiImageRegularBlock, \
    OrganismContentSingleRichTextRegularBlock, OrganismContentSingleVideoRegularBlock, \
    OrganismContentSingleImageRegularBlock, OrganismContentSingleAudioRegularBlock, \
    OrganismContentDoubleQuoteRichTextRegularBlock, OrganismContentDoubleImageRichTextRegularBlock, \
    OrganismLinkListRegularBlock


class MetaHubStoryPage(AbstractMetaHubRichBasePage):
    """
    Page for the stories. These pages are not based on BeeCollect data but all
    made in the CMS.
    """

    pass

    # # Used by Fork to retrieve story pages
    # rest_api_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    #
    # # The header is tightly connected to the introduction component, which inherits its contents
    # hero_header = StreamField([
    #     ('header_image', OrganismHeroHeaderMultiImageRegularBlock()),
    # ])
    #
    # # CMS panels
    # content = StreamField([
    #     ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
    #     ('single_video', OrganismContentSingleVideoRegularBlock()),
    #     ('single_image', OrganismContentSingleImageRegularBlock()),
    #     ('single_audio', OrganismContentSingleAudioRegularBlock()),
    #     ('double_quote_richtext', OrganismContentDoubleQuoteRichTextRegularBlock()),
    #     ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
    # ])
    # related_links = StreamField([('link_block', OrganismLinkListRegularBlock(max_num=1)),], blank=True )
    #
    # content_panels = AbstractMetaHubRichBasePage.content_panels + [
    #     ReadOnlyPanel('rest_api_id', heading="API identifier"),
    #     FieldPanel('collection_category'),
    #     StreamFieldPanel('hero_header'),
    #     StreamFieldPanel('content'),
    #     StreamFieldPanel('related_links'),
    # ]
    #
    # def build_hero_header(self):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Created based on CMS panel, not automatically from BeeCollect.
    #     """
    #     header_child = self.hero_header[0]
    #     component = header_child.block.build_component(header_child.value)
    #     information = self.get_hero_info()
    #     return component._replace(information=information, context=self.has_context())
    #
    # def get_lightbox_items(self):
    #     """
    #     Get lightbox items and information. Since we need access to the properties
    #     of the MetaHubImage object we can't reuse get_object_images for this.
    #     """
    #     data = []
    #     try:
    #         header_child = self.hero_header[0]
    #     except IndexError:
    #         return []
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         for sv in picture_structvalues:
    #             image = sv['source']
    #             image_data = {
    #                 'picture' : AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image)),
    #                 'information': {
    #                    'title' : self.title,
    #                    'name' : '',
    #                    'description': '',
    #                    'credits': image.attribution,
    #                 }
    #             }
    #             data.append(image_data)
    #     return data
    #
    # def get_hero_images(self):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Extracts the chosen images for the hero so that they can be reused in the
    #     intro component and lightbox component as well.
    #     """
    #     try:
    #         header_child = self.hero_header[0]
    #     except IndexError:
    #         return []
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         return [AtomPictureRegular(**Resolution(mobile='1920', crop=True).resolve(sv['source'])) for sv in
    #                 picture_structvalues]
    #
    # def get_first_hero_image(self):
    #     try:
    #         header_child = self.hero_header[0]
    #     except IndexError:
    #         return []
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         return picture_structvalues[0]
    #
    # def get_hero_info(self):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Determines information that is displayed in this page type's hero header.
    #     """
    #     return {
    #         'name' : self.get_category(),
    #         'title' : self.title
    #     }
    #
    # def get_search_representation(self):
    #     """
    #     Renders card for search result views.
    #     """
    #     return self.get_card_representation()
    #
    #
    # def get_card_representation(self, classes=''):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Decides what info to present on the "Discover collection in context" card.
    #     """
    #     return MoleculeContextCardRegular(
    #         href=self.url,
    #         color='blurple',
    #         title=self.get_hero_info()['title'],
    #         type=self.get_category(),
    #         picture=self.get_primary_image(),
    #         classes=classes
    #     )
    #
    # def get_api_compatible_image(self):
    #     """
    #     Extracts MetaHubImage object source from the header so API can call
    #     rendition serializer.
    #     """
    #     try:
    #         header_child = self.hero_header[0]
    #     except IndexError:
    #         return None
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         try:
    #             return picture_structvalues[0]['source']
    #         except IndexError:
    #             return None
    #
    # def get_primary_image(self):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Image that is used if representing the object in a card or other component.
    #     """
    #     images = self.get_hero_images()
    #     if len(images) > 0:
    #         return images[0]
    #     return None
    #
    # def get_elasticsearch_image(self):
    #     """
    #     Used by ElasticSearch, returns the path to the object's first image.
    #     TODO: Handle objects without image, this should return a placeholder ideally
    #     """
    #     image = self.get_first_hero_image()
    #     if image:
    #         try:
    #             image_data = ImageRenditionField('width-400').to_representation(image['source'])
    #             url = image_data['url']
    #         except AttributeError:
    #             return '/static/media/unsplash/cropped/search-result-2.jpg'
    #         else:
    #             return url
    #     return '/static/media/unsplash/cropped/search-result-2.jpg'
    #
    # def get_favourite_info(self):
    #     """
    #     Specifies category and unique identifier for this page.
    #     """
    #     return {
    #         'category' : 'story',
    #         'id': self.pk
    #     }
    #
    # def get_tags_as_list(self):
    #     """
    #     Overrides method from AbstractMetaHubRichBasePage
    #     Used for ES indexing. At the moment stories do not have tags, but
    #     this might be added in the future.
    #     """
    #     return []
    #
    # def save(self, *args, **kwargs):
    #     super().save(**kwargs)
    #
    #     # Set REST API id
    #     if self.id:
    #         self.rest_api_id = "story_{}".format(self.id)
    #         super().save(**kwargs)
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from starling.interfaces.atoms import AtomPictureRegular
from starling.interfaces.generic import Resolution
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from metahub.collection.models import CollectionObjectTag
from metahub.content.blocks import content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.molecules.interfaces import MoleculeObjectCardRegular, MoleculeContextCardRegular
from metahub.starling_metahub.organisms.interfaces import OrganismObjectHeaderRegular, OrganismObjectIntro


class MetaHubObjectPage(MetaHubBasePage):
    """
    Page for the rich collection objects. It defines the object it is related to.
    Through this object we also gain access to the fields such as artist, object
    category etc. The users can add rich content to this page in the CMS.

    There are some read-only fields that allow the user to view this info in the CMS.
    This is probably not the best way to implement this but it does the job for now.

    This class overrides a lot of the methods from MetaHubBasePage. See the
    superclass for an overview of possible overrides.
    """

    # Page object
    object = models.ForeignKey('collection.BaseCollectionObject', null=True, on_delete=models.SET_NULL, blank=True, related_name='associated_page')
    introduction = models.TextField(max_length=2000, blank=True)

    # Maximum of related objects shown
    MAX_RELATED_OBJECTS = 3

    # CMS panels
    content = StreamField(content_blocks(), blank=True)
    tags = ClusterTaggableManager(through=CollectionObjectTag, blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('object'),
        FieldPanel('introduction'),
        StreamFieldPanel('content'),
        FieldPanel('tags'),
        # InlinePanel('obj_img_link')
    ]

    metadata_panels = [
    ]

    # Override tab interface to show metadata panels
    # edit_handler = TabbedInterface([
    #     ObjectList(content_panels, heading='Content'),
    #     ObjectList(metadata_panels, heading='Object metadata'),
    #     ObjectList(Page.promote_panels, heading='Promote'),
    #     ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    # ])


    def get_object_header_component(self):
        return OrganismObjectHeaderRegular(
            title="Sample title until objects are linked",
            subtitle="Sample"
        )

    def get_object_intro_component(self):
        return OrganismObjectIntro(
            text=f"<p>{self.introduction}</p>",
            classes="richtext__section-space--bottom"
        )

    # def build_hero_header(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Creates an image based hero header automatically (cannot be set in CMS) based
    #     on data from BeeCollect.
    #     """
    #     pass
    #     return OrganismHeroHeaderMultiImageRegular(
    #         information=self.get_hero_info(),
    #         expandable=True,
    #         pictures=self.get_object_images(),
    #         theme='white'
    #     )
    #
    # def get_hero_images(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     For this kind of page, images are not chosen in the CMS but are automatically
    #     retrieved from the corresponding object.
    #     """
    #     return self.get_object_images()
    #
    # def get_object_artist(self):
    #     if self.object:
    #         if self.object.artist:
    #             return str(self.object.artist)
    #         else:
    #             return 'Unbekannt'
    #     return None
    #
    # def get_type_dating(self):
    #     date = self.object.datings
    #     dating = ", {}".format(date) if date else ''
    #
    #     type = self.object.object_type
    #     return "{}{}".format(type, dating)
    #
    # def get_hero_info(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Determines information that is displayed in this page type's hero header.
    #     """
    #     if self.get_object_artist():
    #         name = self.get_object_artist()
    #     else:
    #         name = self.get_category()
    #
    #
    #     return {
    #         'name': name,
    #         'title': self.title,
    #         'date': self.get_type_dating()
    #     }
    #
    # def get_tags(self):
    #     """
    #     Generates the frontend-compatible list of tags. These are the tags from the
    #     django-taggit model, and can be managed in the CMS.
    #     """
    #     if self.tags and len(self.tags.all()) > 0:
    #         searchpage = self.get_search_base_url()
    #         tags = { 'title' : 'Schlagworte', 'tag_items' : [ {'title': str(tag), 'href': '{}?id_tags={}'.format(searchpage, str(tag)) } for tag in self.tags.all()] }
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
    # def get_primary_image(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Image that is used if representing the object in a card or other component.
    #     TODO: return a default image if not found (objects without image can exist)
    #     """
    #     images = self.get_object_images()
    #     if images:
    #         return images[0]
    #     # Return default image
    #     else:
    #         return None
    #
    # def get_raw_images(self):
    #     """
    #     Overrides method from MetaHubBasePage
    #     Used when we need the raw images and not the atomized variant.
    #     """
    #     if self.object:
    #        if self.object.bc_image_license:
    #            #no copyrighted images!
    #            if self.object.bc_image_license.find('©') != -1 or self.object.bc_image_license.find('(c)') != -1:
    #                return []
    #        image_links = self.object.obj_img_link.all()
    #        return [link.object_image for link in image_links]
    #     return []
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
    #         date=self.object.datings,
    #         classes=classes,
    #     )
    #
    # def get_lightbox_items(self):
    #     """
    #     Get lightbox items and information. Since we need access to the properties
    #     of the MetaHubImage object we can't reuse get_object_images for this.
    #     """
    #     data = []
    #     if self.object:
    #        image_links = self.object.obj_img_link.all()
    #        for image_link in image_links:
    #            image = image_link.object_image
    #            image_data = {
    #                'picture' : AtomPictureRegular(**Resolution(mobile='2048', landscape='4096', crop=True).resolve(image)),
    #                'information': {
    #                    'title' : self.title,
    #                    'name' : self.get_object_artist(),
    #                    'description': '', #image.alt_text, #MKR this is wrong, but what else to show here?
    #                    'credits': image.attribution,
    #                }
    #            }
    #            data.append(image_data)
    #     return data
    #
    # def get_object_images(self):
    #     """
    #     Retrieve all images belonging to this page's linked object and transform them
    #     into a frontend component. Can be passed to heroimage/slideshow components.
    #     """
    #     if self.object:
    #        images = self.object.obj_img_link.all()
    #        return [AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image.object_image)) for image in
    #                 images]
    #     return []
    #
    # def build_metadata(self):
    #     """
    #     Creates the right format that the frontend accepts for the object metadata fields.
    #     The information displayed here is based on BeeCollect data and not managable in the
    #     CMS, though it can be viewed in the metadata tab.
    #     TODO: Support localization , lol
    #     """
    #     if self.object:
    #         return [
    #             {
    #                 'title': 'Basisdaten',
    #                 'information': self.object.get_metadata_information_fields()
    #             },
    #             {
    #                 'title' : 'Eigentum und Erwerbung',
    #                 'information' : self.object.get_metadata_property_inheritance_fields()
    #             },
    #             {
    #                 'title': 'Ausstellungen',
    #                 'information': self.object.get_metadata_display_fields()
    #             }
    #         ]
    #     else:
    #         return []
    #
    # def build_related_objects(self):
    #     """
    #     Determine what objects should be shown in the related objects component.
    #     Maximum of 4. Checks for: same artist, same tags, same material, same category.
    #     """
    #     no_related_found = False
    #     page_pool = MetaHubObjectPage.objects.live().exclude(pk=self.pk)
    #
    #     # First check for the same artist, if it has one
    #     related_pages = []
    #
    #     if self.object.artist:
    #         results = page_pool.distinct().filter(object__artist=self.object.artist,
    #                                    object__object_type=self.object.object_type,
    #                                    tags__name__in=self.tags.all())
    #     else:
    #         results = page_pool.distinct().filter(object__object_type=self.object.object_type,
    #                                    tags__name__in=self.tags.all())
    #
    #     # Nothing found, use random?
    #     if len(results) == 0:
    #         results = page_pool.distinct()
    #         no_related_found = True
    #
    #     # Get random 4 objects
    #     tries = 0
    #     while tries < 100 and len(related_pages) < 4:
    #         new_page = randomchoice(results)
    #         if new_page not in related_pages:
    #             related_pages.append(new_page)
    #         tries += 1
    #
    #     # Fill up with the rest if nothing found or too many tries
    #     if len(related_pages) < 4:
    #         needed = len(related_pages) - 4
    #         existing = [p.pk for p in related_pages]
    #         others = page_pool.distinct().exclude(pk__in=existing)
    #
    #         # Append random objects
    #         if others:
    #             tries = 0
    #             while tries < 100 and len(related_pages) < 4:
    #                 new_page = randomchoice(others)
    #                 if new_page not in related_pages:
    #                     related_pages.append(new_page)
    #                 tries += 1
    #
    #             # Not strictly related anymore
    #             no_related_found = True
    #
    #     cards = []
    #     for related_page in related_pages:
    #         cards.append(related_page.get_object_card_representation())
    #
    #     return OrganismRelatedItemsRegular(
    #         title='Andere Objekte' if no_related_found else 'Verwandte Objekte',
    #         related_objects=cards
    #         )
    #
    #
    # def get_favourite_info(self):
    #     """
    #     Specifies category and unique idenfifier for this page.
    #     """
    #     return {
    #         'category' : 'object',
    #         'id': self.pk,
    #     }
    #
    # def save(self, *args, **kwargs):
    #     super().save(**kwargs)
    #
    #     # If saving for the first time after creation,
    #     # add tags from the BeeCollect object to django-taggit
    #     # MKR , maybe also when not saving for the first time...
    #
    #     if self.pk:
    #         # not foolproof in checking, but for now fine, so the only way to add tags is from beecollect! otherwise no way to tell changes
    #         if len(self.object.get_bc_tags_as_list()) != len(self.tags.all()):
    #             for t in self.tags.all():
    #                 t.delete()
    #         if len(self.tags.all()) == 0:
    #             self.tags.set(*self.object.get_bc_tags_as_list())
    #         super().save(**kwargs)
    #
    # def get_context(self, request, *args, **kwargs):
    #     # Required to avoid circular imports
    #     context = super(MetaHubObjectPage, self).get_context(request, *args, **kwargs)
    #     context['bc'] = request.GET.get('c','')  #bodyclass for testing
    #     return context
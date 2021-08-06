from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.contrib.taggit import ClusterTaggableManager
from starling.interfaces.atoms import AtomPictureRegular
from starling.interfaces.generic import Resolution
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet

from metahub.collection.models import CollectionObjectTag
from metahub.content.blocks import content_blocks
from metahub.core.models import MetaHubBasePage, MetahubImage
from metahub.starling_metahub.molecules.interfaces import MoleculeObjectCardRegular, MoleculeContextCardRegular, \
    MoleculeCardRegular, MoleculeExploreCardRegular
from metahub.starling_metahub.organisms.blocks import OrganismArticleCuratedItemsRegularBlock, \
    OrganismArticleRelatedItemsRegularBlock, OrganismArticleCuratedObjectsRegularBlock, \
    OrganismArticleRelatedObjectsRegularBlock
from metahub.starling_metahub.organisms.interfaces import OrganismObjectHeaderRegular, OrganismObjectIntroRegular, \
    OrganismObjectMetadataRegular


@register_snippet
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
    parent_page_types = ['overviews.MetaHubOverviewPage']

    object = models.ForeignKey('collection.BaseCollectionObject', null=True, on_delete=models.SET_NULL, blank=True, related_name='associated_page')
    subtitle = models.CharField(max_length=500, blank=True, default='')
    introduction = models.TextField(max_length=2000, blank=True)
    location_page = models.ManyToManyField('locations.MetaHubLocationPage', related_name='object_pages', blank=True, null=True)

    # Maximum of related objects shown
    MAX_RELATED_OBJECTS = 3

    # CMS panels
    content = StreamField(content_blocks(), blank=True)
    tags = ClusterTaggableManager(through=CollectionObjectTag, blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedObjectsRegularBlock()),
        ('related_automatic', OrganismArticleRelatedObjectsRegularBlock()),
    ], blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('object'),
            FieldPanel('subtitle', help_text="Leave blank to use artist (if present)"),
            FieldPanel('introduction'),
            FieldPanel('location_page'),
        ], heading="Basic information"),
        StreamFieldPanel('content'),
        FieldPanel('tags'),
        StreamFieldPanel('related_items')
    ]


    def get_object_image(self):
        # todo, this is temp since there are no real objects
        return AtomPictureRegular(**Resolution(mobile='1920', crop=True).resolve(MetahubImage.objects.first()))

    def get_object_header_component(self):
        return OrganismObjectHeaderRegular(
            title=self.title,
            subtitle=self.get_object_subtitle()
        )

    def get_object_subtitle(self):
        return self.subtitle

    def get_object_intro_component(self):
        return OrganismObjectIntroRegular(
            text=f"<p>{self.introduction}</p>",
            classes="richtext__section-space--bottom"
        )

    def get_object_metadata(self):
        # Douwe
        # We can use the method below once the actual object exists
        # Check what metadata fields are for metahub since it still uses JMF ones
        # items = self.object.get_metadata_information_fields()
        items = [
            {
                'title': 'Title',
                'data': 'Etrog liqueur',
            },
            {
                'title': 'Kunstler in Hersteller in',
                'data': 'Kurt de Jong',
            },
            {
                'title': 'Datierung',
                'data': '2007',
            },
            {
                'title': 'Objektbezeichnung',
                'data': 'bottle',
            },
            {
                'title': 'Ort',
                'data': 'Frankfurt am Main',
            },
            {
                'title': 'MaBe',
                'data': 'Bottle 1:30cm',
            },
            {
                'title': 'Material Technik',
                'data': 'Glass',
            },
            {
                'title': 'Signatur',
                'data': 'JMF contemporary cultures',
            }
        ]

        for index, item in enumerate(items):
            item['number'] = str(index+1).zfill(2)

        return items

    def get_object_metadata_component(self):
        return OrganismObjectMetadataRegular(
            items=self.get_object_metadata()
        )

    def get_page_label(self):
        return _('Object')

    def get_card_representation(self):
        return MoleculeExploreCardRegular(
            title=self.title,
            label=self.get_page_label(),
            subtitle=self.get_object_subtitle(),
            theme_color=self.theme_color,
            href=self.url,
            picture=self.get_object_image(),
            type='object'
        )


    def get_page_related_items(self):
        # Douwe
        # TODO this is itself for now since we dont have real objects yet
        # The old implementation is below but not sure how useful it is
        return [self, self, self]

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

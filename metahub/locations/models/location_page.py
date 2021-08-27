from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmodelchooser.blocks import ModelChooserBlock

from metahub.content.blocks import cookieless_content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.molecules.interfaces import MoleculeExploreCardRegular
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismHeroTextHeaderExtraInfoBlock, OrganismArticleCuratedStoriesRegularBlock, \
    OrganismArticleRelatedStoriesRegularBlock
from metahub.starling_metahub.organisms.interfaces import OrganismArticleRelatedItemsRegular


class LocationObjectRelationship(Orderable, models.Model):
    """Intermediate table for holding the many-to-many relationship. """
    location = ParentalKey('MetaHubLocationPage', related_name='location_object_relationship', on_delete=models.CASCADE)
    object = models.ForeignKey('collection.MetaHubObjectPage', related_name='object_location_relationship', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('object')
    ]


class MetaHubLocationPage(MetaHubBasePage):
    """
    Page for the locations. These pages are not based on BeeCollect data but all
    made in the CMS. Location is basically the same as a story page.
    """
    parent_page_types = ['overviews.MetaHubOverviewPage']

    authors = StreamField([
        ('author', ModelChooserBlock(target_model='authors.Author', icon='user'))
    ], blank=True)

    date = models.DateField(blank=True, null=True)
    latitude = models.CharField(blank=True, max_length=200)
    longitude = models.CharField(blank=True, max_length=200)

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ])
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderExtraInfoBlock()),
    ])

    content = StreamField(cookieless_content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedStoriesRegularBlock()),
        ('related_automatic', OrganismArticleRelatedStoriesRegularBlock()),

    ], blank=True)

    tags = ClusterTaggableManager(through='locations.LocationTag', blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        MultiFieldPanel([
            FieldPanel('date'),
            StreamFieldPanel('authors'),
        ], heading=_("Publishing information")),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
            InlinePanel('location_object_relationship', label=_("Associated Object(s)"), panels=None, min_num=1)
        ], heading=_("Location specifics")),
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading=_("Page Header")),
        StreamFieldPanel('content'),
        # StreamFieldPanel('related_items'),
        FieldPanel('tags')
    ]

    @property
    def associated_objects(self):
        return [n.object for n in self.location_object_relationship.all()]

    def get_associated_objects_component(self):
        return OrganismArticleRelatedItemsRegular(
            title=_("Objects for this location"),
            cards=[o.get_card_representation() for o in self.associated_objects]
        )

    def get_page_related_items(self):
        return MetaHubLocationPage.objects.live().exclude(pk=self.pk)[:3]

    def get_page_label(self):
        return _('Location')

    def get_page_type(self):
        return 'story' # uses same card renderings

    def get_card_representation(self):
        return MoleculeExploreCardRegular(
            title=self.title,
            label=self.get_page_label(),
            subtitle="TODO wat komt hier?",
            href=self.url,
            picture=self.get_page_header_image(),
            type=self.get_page_type(),
            theme_color=self.theme_color
        )
    #
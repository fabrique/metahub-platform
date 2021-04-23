from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.images.api.fields import ImageRenditionField


class BaseTag(models.Model):
    """
    Tag attached to the OBJECT MODEL. The tags come out of BeeCollect in the form
    of a comma-separated string. We store these original tags with this model.
    Each object can have multiple tags and each tag can belong to multiple objects.
    """
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class CollectionObjectTag(TaggedItemBase):
    """
    Tag attached to the OBJECT PAGE, these tags are inferred from BeeCollect
    upon import but can also be changed and added upon in the CMS.
    """
    content_object = ParentalKey(
        'core.MetaHubObjectPage',
        related_name='tagged_objects',
        on_delete=models.CASCADE,
    )


class CollectionObjectSeriesTag(TaggedItemBase):
    """
    Tag attached to the OBJECT SERIES PAGE. These are an aggregate of the objects
    that are a part of this series, and created at sync time. They can be changed
    and expanded upon in the CMS.
    """
    content_object = ParentalKey(
        'core.MetaHubObjectSeriesPage',
        related_name='tagged_object_series',
        on_delete=models.CASCADE,
    )


class BaseCollectionArtist(models.Model):
    """
    Artist model based on the data from BeeCollect. Properties that are important
    to BeeCollect only are preceded by bc. Objects can be related to 1 Artist only.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    bc_inventory_number = models.CharField(max_length=1024)
    bc_date_acquired = models.CharField(max_length=256)
    bc_change_user = models.CharField(max_length=256)
    bc_change_date = models.CharField(max_length=256)
    bc_dating = models.CharField(max_length=256)

    type = models.CharField(max_length=256)
    first_name = models.CharField(max_length=1024, default='')
    last_name = models.CharField(max_length=1024, default='')
    alias_name = models.CharField(max_length=1024, default='')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class BaseCollectionObject(ClusterableModel):
    """
    Object model based on the data from BeeCollect. Properties that are important
    to BeeCollect only are preceded by bc. Objects can contain an artist relation,
    series relation and tag relation.
    """

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Original specific BeeCollect data
    bc_id = models.IntegerField()
    bc_inventory_number = models.CharField(max_length=1024, default='', blank=True)
    bc_change_user = models.CharField(max_length=256, default='', blank=True)
    bc_change_date = models.CharField(max_length=256, default='', blank=True)
    bc_object_name = models.CharField(max_length=256, default='', blank=True)
    bc_images = models.CharField(max_length=1024, default='', blank=True)
    bc_image_license = models.CharField(max_length=256, default='', blank=True)

    # Extra BeeCollect content
    bc_notes = models.CharField(max_length=4024, default='', blank=True)
    bc_credits = models.CharField(max_length=1024, default='', blank=True)
    bc_tags = models.CharField(max_length=1024, default='', blank=True)
    bc_tags_separate = models.ManyToManyField('collection.BaseTag', blank=True, related_name='attached_objects')
    tag_synonyms = models.CharField(max_length=10000, default='')
    publications = models.CharField(max_length=1024, default='', blank=True)

    # Dating and origin/acquisition
    date_acquired = models.CharField(max_length=256, default='', blank=True)
    datings = models.CharField(max_length=1024, default='', blank=True)
    dating_from_df = models.DateField(blank=True, null=True)
    dating_to_df = models.DateField(blank=True, null=True)
    provenance = models.CharField(max_length=1024, default='', blank=True)
    is_highlight = models.BooleanField(default=False)

    # Series/categorization
    convolute = models.CharField(max_length=256, default='', blank=True)
    series_id = models.CharField(null=True, blank=True, max_length=256)
    series_page = models.ForeignKey('core.MetaHubObjectSeriesPage', null=True, blank=True, on_delete=models.SET_NULL, related_name='collection_objects')

    # Location of object
    container_name = models.CharField(max_length=1024, default='', blank=True)
    container_id = models.CharField(max_length=256, default='', blank=True)
    current_location = models.CharField(max_length=256, default='', blank=True)
    geographic_location = models.CharField(max_length=1024, default='', blank=True)

    # Object itself
    title = models.CharField(max_length=1024, default='', blank=True, verbose_name='Titel')
    description = models.CharField(max_length=1024, default='', blank=True)
    signatures = models.CharField(max_length=1024, default='', blank=True, verbose_name='Signatur')
    object_type = models.CharField(max_length=1024, default='', blank=True, verbose_name='Objektbezeichnung')
    artist = models.ForeignKey(BaseCollectionArtist, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Künstler')

    # Physicalities
    material = models.CharField(max_length=1024, blank=True)
    dimensions = models.CharField(max_length=1024, blank=True)

    # Also rendered in CMS
    def __str__(self):
        return '{}, {}, {}'.format(self.title, self.bc_inventory_number, self.pk)

    def get_elasticsearch_image(self):
        """
        Used by ElasticSearch, returns the path to the object's first image.
        TODO: Handle objects without image, this should return a placeholder ideally
        TODO: However the placeholder should probably be defined at object level rather than here
        """
        if self.obj_img_link:
            first_image_link = self.obj_img_link.first()

            try:
                image = first_image_link.object_image
                image_data = ImageRenditionField('width-400').to_representation(image)
                url = image_data['url']
            except AttributeError:
                return '/static/media/unsplash/cropped/search-result-2.jpg'
            else:
                return url
        return '/static/media/unsplash/cropped/search-result-2.jpg'

    def artist_to_string(self):
        return str(self.get_artist())

    def get_object_type(self):
        return 'Objekt'

    def get_object_page_tags(self):
        if self.associated_page.first():
            return self.associated_page.first().get_tags_as_list()
        return []

    def get_object_page_url(self):
        # TODO: return 404 if not found?
        if self.associated_page:
            try:
                url = self.associated_page.first().url
            except AttributeError:
                return '/'
            else:
                return url
        else:
            return '/'

    def get_is_highlight(self):
        if self.associated_page:
            try:
                return self.associated_page.first().is_highlight
            except AttributeError:
                return False

    @property
    def live(self):
        if self.associated_page:
            return self.associated_page.first().live
        return False

    def get_series_page_id(self):
        """
        Used to generate prefiltered search results based on a series page
        and its objects. Since users can make series themselves we do this
        on page basis, not on series_id field since this is from BeeCollect.
        """
        if self.series_page:
            return self.series_page.get_elasticsearch_series_id()
        return None

    def get_artist(self):
        if self.artist is not None:
            return self.artist
        else:
            return 'Unbekannt'

    def get_bc_tags_as_list(self):
        if self.bc_tags:
            return self.bc_tags.split('|')
        else:
            return []

    def only_take_existing_data(self, fields):
        """
        Parses the metadata and only keeps fields that contain data.
        """
        list = []
        for el in fields:
            if el['value'] and el['value'] != '':
                list.append(el)
        return list

    def get_metadata_information_fields(self):
        """
        Mapping method used to create the list of metadata that is shown on the object
        (series) page. Since we only want existing/filled fields we do it like this.
        TODO: see if it can be improved (list comprehension?)
        TODO: localization support
        """
        fields = (
            {
                'value': self.title,
                'name': 'Titel'
            },
            {
                'value': self.get_artist(),
                'name': 'Künstler*in / Hersteller*in'
            },
            {
                'value': self.datings,
                'name': 'Datierung'
            },
            {
                'value': self.object_type,
                'name': 'Objektbezeichnung'
            },
            {
                'value': self.container_name,
                'name': 'Sammlungsbereich'
            },
            {
                'value': self.geographic_location,
                'name': 'Ort'
            },
            {
                'value': self.dimensions,
                'name': 'Maße'
            },
            {
                'value': self.material,
                'name': 'Material / Technik'
            },
            {
                'value': self.signatures,
                'name': 'Signatur / Beschriftung'
            },
            {
                'value': self.publications,
                'name': 'Literatur'
            },
            {
                'value': self.bc_image_license,
                'name': 'Bildlizenz'
            },
        )
        return self.only_take_existing_data(fields)

    def get_metadata_property_inheritance_fields(self):
        """
        Mapping method used to create the list of metadata that is shown on the object
        (series) page. Since we only want existing/filled fields we do it like this.
        TODO: localization support
        """
        fields =  (
            {
                'value': self.date_acquired,
                'name' : 'Erwerbsdatum'

            },
            {
                'value': self.bc_credits,
                'name': 'Leihgeber*in'
            },
            {
                'value': self.provenance,
                'name': 'Vorbesitz'
            },
            {
                'value': self.bc_inventory_number,
                'name': 'Inventarnummer'
            },
        )
        return self.only_take_existing_data(fields)

    def get_metadata_display_fields(self):
        """
        Mapping method used to create the list of metadata that is shown on the object
        (series) page. Since we only want existing/filled fields we do it like this.
        TODO: localization support
        """
        fields = (
            {
                'value': self.current_location,
                'name': 'Ausgestellt'
            },
        )
        return self.only_take_existing_data(fields)


class ObjectImageLink(models.Model):
    """
    In-between model to handle relationship between objects and images. Upon import,
    all these relationships are deleted and then reconstructed based on the import data.
    """
    collection_object = models.ForeignKey('collection.BaseCollectionObject', related_name='obj_img_link', on_delete=models.CASCADE)
    object_image = models.ForeignKey('core.metahubImage', related_name='obj_img_link', on_delete=models.CASCADE)


class CollectionCategory(models.Model):
    """
    Represents the different areas of the MetaHub collection, such as Objekt, Objektseries,
    Geschichten etc. A Story/Object/Series page belongs to one of these categories.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paginacategorie'
        verbose_name_plural = 'Paginacategorieen'
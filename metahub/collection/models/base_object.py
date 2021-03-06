from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.images.api.fields import ImageRenditionField


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
    # series_page = models.ForeignKey('collection.MetaHubObjectSeriesPage', null=True, blank=True, on_delete=models.SET_NULL, related_name='collection_objects')

    # Location of object
    container_name = models.CharField(max_length=1024, default='', blank=True)
    container_id = models.CharField(max_length=256, default='', blank=True)
    current_location = models.CharField(max_length=256, default='', blank=True)
    geographic_reference = models.CharField(max_length=1024, default='', blank=True)
    geographic_location = models.CharField(max_length=1024, default='', blank=True)

    # Object itself
    title = models.CharField(max_length=1024, default='', blank=True, verbose_name='Titel')
    description = models.CharField(max_length=1024, default='', blank=True)
    signatures = models.CharField(max_length=1024, default='', blank=True, verbose_name='Signatur')
    object_type = models.CharField(max_length=1024, default='', blank=True, verbose_name='Objektbezeichnung')
    artist = models.ForeignKey('collection.BaseCollectionArtist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='K??nstler')

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

    @property
    def live(self):
        if self.associated_page:
            return self.associated_page.first().live
        return False

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
            if el['data'] and el['data'] != '':
                list.append(el)
        return list

    def get_metadata_information_fields(self):
        """
        Mapping method used to create the list of metadata that is shown on the object
        (series) page. Since we only want existing/filled fields we do it like this.
        TODO: see if it can be improved (list comprehension?)
        """
        fields = (
            {
                'data': self.title,
                'title': 'Titel'
            },
            {
                'data': str(self.artist) if self.artist else '',
                'title': 'Kunstler(in) / Hersteller(in)'
            },
            {
                'data': self.datings,
                'title': 'Datierung'
            },
            {
                'data': self.object_type,
                'title': 'Objektbezeichnung'
            },
            {
                'data': self.container_name,
                'title': 'Sammlungsbereich'
            },
            {
                'data': self.geographic_location,
                'title': 'Ort'
            },
            {
                'data': self.dimensions,
                'title': 'Ma??e'
            },
            {
                'data': self.material,
                'title': 'Material / Technik'
            },
            {
                'data': self.signatures,
                'title': 'Signatur / Beschriftung'
            },
            {
                'data': self.bc_image_license,
                'title': 'Bildlizenz'
            }
        )
        return self.only_take_existing_data(fields)


class ObjectImageLink(models.Model):
    """
    In-between model to handle relationship between objects and images. Upon import,
    all these relationships are deleted and then reconstructed based on the import data.
    """
    collection_object = models.ForeignKey('collection.BaseCollectionObject', related_name='object_img_link', on_delete=models.CASCADE)
    object_image = models.ForeignKey('core.MetahubImage', related_name='object_img_link', on_delete=models.CASCADE)
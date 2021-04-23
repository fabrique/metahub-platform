from datetime import datetime

from django.utils.text import slugify
from wagtail.core.models import Page

from metahub.collection.models import BaseCollectionArtist, BaseCollectionObject, ObjectImageLink, CollectionCategory, BaseTag
from metahub.core.models import MetaHubObjectPage, MetaHubObjectSeriesPage, MetaHubCategoryOverviewPage
from metahub.sync.models import BeeCollectSyncOccurrence
from metahub.sync.utils import add_fabrique_image, add_stream_child


class BeeCollectMapping:
    """
    Maps data from BeeCollect to our corresponding database objects.
    TODO: Generate log output the proper way
    """

    def __init__(self, data):
        self.data = data
        self.artists_added, self.artists_changed, self.artists_removed = 0, 0, 0
        self.objects_added, self.objects_changed, self.objects_removed = 0, 0, 0
        self.create_base_log()

    def create_base_log(self):
        # date of import attempt
        # date of bc data
        self.log = BeeCollectSyncOccurrence(
            date_data_dump=self.data.get('ExportDate'),
            objects_in_dump=self.data.get('NumberOfObjects'),
            artists_in_dump=self.data.get('NumberOfArtists'),
        )
        self.log.save()

    def create_final_log(self):
        self.log.artists_added = self.artists_added
        self.log.artists_changed = self.artists_changed
        self.log.artists_removed = self.artists_removed
        
        self.log.objects_added = self.objects_added
        self.log.objects_changed = self.objects_changed
        self.log.objects_removed = self.objects_removed

        self.log.save()

    def get_or_create_object(self, object_data, update=False):
        """
        Tries to retrieve the object first by the BeeCollect Id. This should be unique.
        If it does not exist, it will be created, where each property will call its own
        mapping function if necessary.
        """
        bc_id = object_data.get('Id')

        bco = BaseCollectionObject.objects.filter(bc_id=bc_id)
        if len(bco) > 0:
            exists = True
        else:
            exists = False

        if exists:
            if update:
                bco.update(
                    bc_id=object_data.get('Id'),
                    bc_inventory_number=object_data.get('InventoryNumber'),
                    bc_change_date=object_data.get('ChangeDate'),
                    bc_change_user=object_data.get('ChangeUser'),
                    bc_object_name=object_data.get('ObjectName'),
                    bc_credits=object_data.get('Creditline'),
                    bc_notes=object_data.get('Notes'),
                    bc_tags='|'.join(self.get_object_keywords_as_list(object_data)),
                    bc_images=self.get_images(object_data.get('Images')),
                    bc_image_license=self.get_image_licenses(object_data.get('Images')),

                    date_acquired=object_data.get('AcquisitionDate'),
                    datings=self.get_datings_str(object_data.get('Datings')),
                    dating_from_df=self.get_datings_from(object_data.get('Datings')),
                    dating_to_df=self.get_datings_to(object_data.get('Datings')),
                    provenance=self.get_provenance(object_data.get('Provenance')),
                    signatures=self.get_signatures(object_data.get('Signatures')),
                    publications=self.get_publications(object_data.get('Publications')),
                    is_highlight=object_data.get('IsHighlight', False),

                    current_location=object_data.get('CurrentLocation'),
                    container_name=object_data.get('ContainerName'),
                    container_id=object_data.get('ContainerId'),
                    geographic_location=self.get_geographic_location(object_data.get('Keywords')),

                    convolute=object_data.get('Convolute'),
                    series_id=self.get_series_id(object_data),
                    material=self.get_material(object_data.get('Material_Technique')),
                    dimensions=self.get_dimensions(object_data.get('Dimensions')),
                    title=object_data.get('Title'),
                    artist=self.get_artist_for_object(object_data),
                    object_type=self.get_object_category(object_data),
                )
                self.objects_changed += 1
            return bco.first()

        else:
            new_bco = BaseCollectionObject(
                bc_id=object_data.get('Id'),
                bc_inventory_number=object_data.get('InventoryNumber'),
                bc_change_date=object_data.get('ChangeDate'),
                bc_change_user=object_data.get('ChangeUser'),
                bc_object_name=object_data.get('ObjectName'),
                bc_credits=object_data.get('Creditline'),
                bc_notes=object_data.get('Notes'),
                bc_tags='|'.join(self.get_object_keywords_as_list(object_data)),
                bc_images=self.get_images(object_data.get('Images')),
                bc_image_license=object_data.get('ImageLicense', 'No license specified'),

                date_acquired=object_data.get('AcquisitionDate'),
                datings=self.get_datings_str(object_data.get('Datings')),
                dating_from_df=self.get_datings_from(object_data.get('Datings')),
                dating_to_df=self.get_datings_to(object_data.get('Datings')),
                provenance=self.get_provenance(object_data.get('Provenance')),
                signatures=self.get_signatures(object_data.get('Signatures')),
                publications=self.get_publications(object_data.get('Publications')),
                is_highlight=object_data.get('IsHighlight', False),

                current_location=object_data.get('CurrentLocation'),
                container_name=object_data.get('ContainerName'),
                container_id=object_data.get('ContainerId'),
                geographic_location=self.get_geographic_location(object_data.get('Keywords')),

                convolute=object_data.get('Convolute'),
                series_id=self.get_series_id(object_data),
                material=self.get_material(object_data.get('Material_Technique')),
                dimensions=self.get_dimensions(object_data.get('Dimensions')),
                title=object_data.get('Title'),
                artist=self.get_artist_for_object(object_data),
                object_type=self.get_object_category(object_data),
            )
            new_bco.save()
            self.objects_added += 1
            
            return new_bco

    def add_object_images(self, object_data, object_instance):
        for image in object_data.get('Images'):
            path = image.get('KeyFileName')
            if path:
                try:
                    image = add_fabrique_image(path, overwrite=True, attribution=image.get('License'), alt_text=object_data.get('Title'))
                except FileNotFoundError:
                    print('Image not found')
                else:
                    # Link with object-image-link
                    oil = ObjectImageLink(object_image=image, collection_object=object_instance)
                    oil.save()

    def get_artist_for_object(self, object_data):
        """
        Artists have been added to the DB before objects are synced, so normally
        every object that mentions an artist can find the match.
        """
        creators = object_data.get('Creators')
        artist_id = creators[0].get('ArtistId') if creators else None

        print('fetching artist', artist_id)
        try:
            artist = BaseCollectionArtist.objects.get(bc_inventory_number=artist_id)
            print('Found artist {} for object {}'.format(artist, object_data.get('InventoryNumber')))
        except BaseCollectionArtist.DoesNotExist:
            print('Cannot find artist with id {} for object {}'.format(artist_id, object_data.get('InventoryNumber')))
            artist = None
        return artist

    def get_or_create_artist(self, artist_data, update=False):
        """
        Tries to retrieve the artist by beecollect id. If it does not exist yet,
        creates it. Existing artists can be updated.
        """
        bc_id = artist_data.get('Id')

        artist = BaseCollectionArtist.objects.filter(bc_inventory_number=bc_id)
        if len(artist) > 0:
            exists = True
        else:
            exists = False

        if exists:
            if update:
                artist.update(bc_inventory_number=artist_data.get('Id'),
                    bc_date_acquired=artist_data.get('CreateDate'),
                    bc_change_date=artist_data.get('ChangeDate'),
                    bc_change_user=artist_data.get('ChangeUser'),
                    bc_dating=artist_data.get('Dating'),
                    type=artist_data.get('Type'),
                    first_name=artist_data.get('FirstName').strip(),
                    last_name=artist_data.get('LastName').strip(),
                    alias_name=artist_data.get('AliasName').strip())
                self.artists_changed += 1
            return artist.first()

        else:
            bca = BaseCollectionArtist(
                    bc_inventory_number=artist_data.get('Id'),
                    bc_date_acquired=artist_data.get('CreateDate'),
                    bc_change_date=artist_data.get('ChangeDate'),
                    bc_change_user=artist_data.get('ChangeUser'),
                    bc_dating=artist_data.get('Dating'),
                    type=artist_data.get('Type'),
                    first_name=artist_data.get('FirstName').strip(),
                    last_name=artist_data.get('LastName').strip(),
                    alias_name=artist_data.get('AliasName').strip(),
                )
            bca.save()
            self.artists_added += 1
            
            return bca

    def get_or_create_tag_m2m(self, tag, object_instance):
        """
        Checks whether tag is already attached to model, exists but is not
        attached, or must be created from scratch.
        """
        try:
            return object_instance.bc_tags_separate.get(name=tag)
        except BaseTag.DoesNotExist:
            try:
                tag_to_add = BaseTag.objects.get(name=tag)
            except BaseTag.DoesNotExist:
                tag_to_add = BaseTag(
                    name=tag
                )
            return tag_to_add

    def get_or_create_category(self, category_name):
        """
        Category defined by us, such as Geschichten, Objekt, etc. This is not
        from BeeCollect.
        """
        try:
            return CollectionCategory.objects.get(name=category_name)
        except CollectionCategory.DoesNotExist:
            c = CollectionCategory(name=category_name, description='').save()
            return c

    def get_object_category(self, object_data):
        """
        This field is rather dirty so requires some equally dirty code to
        get the right data out.
        """
        object_keywords = object_data.get('Keywords')
        for k in object_keywords:
            if k['Type'] == 'Objektbezeichnung':
                if k.get('Text'):
                    try:
                        category_clean = k.get('Text').split('(')[0].strip()
                    except IndexError:
                        return 'Unbekannt'
                    else:
                        return category_clean
        return 'Unbekannt'

    def get_object_keywords_as_list(self, bc_object):
        """
        The object keywords are not presented neatly in the data. Some might
        also contain commas, hence not making it safe to store as a comma
        separated string if you intend on splitting that again later.
        """
        keywords = []
        object_keywords = bc_object.get('Keywords')
        for k in object_keywords:
            if k.get('Type') == 'Inhalt/Kontext':
                if k.get('Text'):
                    try:
                        keyword_clean = k.get('Text').split('(')[0].strip()
                    except IndexError:
                        continue
                    else:
                        keywords.append(keyword_clean)
        return keywords

    def add_tags_to_object(self, bc_object, object_instance):
        tag_list = self.get_object_keywords_as_list(bc_object)
        for tag in tag_list:
            self.get_or_create_tag_m2m(tag, object_instance)

    def get_publications(self, publications_list):
        publications = []
        for publication in publications_list:
            specifications = []

            if publication.get('Text'):
                for key, value in publication.items():
                    if key != 'Text' and value != '':
                        specifications.append(value)

                text = publication.get('Text').strip()

                if text:
                    spec_text = "- {}".format(self.comma_separated(specifications)) if specifications else ''
                    publications.append("{}{}".format(text, spec_text))

        return self.comma_separated(publications)

    def get_image_licenses(self, image_list):
        images = []
        for image in image_list:
            images.append(image.get('License'))

        return self.comma_separated(images)

    def get_images(self, image_list):
        images = []
        for image in image_list:
            images.append(image.get('KeyFileName'))

        return self.comma_separated(images)

    def comma_separated(self, list):
        if list:
            return ', '.join(list)
        return ''

    def get_signatures(self, signatures_list):
        signatures = []
        for signature in signatures_list:
            if signature.get('Text') and signature.get('Type'):
                signatures.append("{} {}".format(signature.get('Text'), signature.get('Type')))
        return self.comma_separated(signatures)

    def get_material(self, material_list):
        materials = []
        for entry in material_list:
            material = entry.get('Text')
            if material:
                materials.append(material)

        return self.comma_separated(materials)

    def get_dimensions(self, dimension_list):
        dimensions = []
        for entry in dimension_list:
            dimensions.append(entry.get('Text'))
        return self.comma_separated(dimensions)

    def get_datings_str(self, datings_list):
        """
        Gets datings in 1900-2000 format.
        TODO: Localization support?
        """
        if datings_list:
            try:
                datings = datings_list[0]
            except IndexError:
                return 'Unbekannt'
            else:
                return datings.get('Text', 'Unbekannt')
        else:
            return 'Unbekannt'

    def get_datings_from(self, datings_list):
        if datings_list:
            try:
                datings_from = datings_list[0].get('YearFrom')
            except IndexError:
                return None
            else:
                try:
                    year = int(datings_from)
                except ValueError:
                    return None
                else:
                    date_string = '1-1-{}'.format(year)
                    return datetime.strptime(date_string, "%d-%m-%Y").date()

    def get_datings_to(self, datings_list):
        if datings_list:
            try:
                datings_to = datings_list[0].get('YearTo')
            except IndexError:
                return None
            else:
                try:
                    year = int(datings_to)
                except ValueError:
                    return None
                else:
                    date_string = '1-1-{}'.format(year)
                    return datetime.strptime(date_string, "%d-%m-%Y").date()

    def get_provenance(self, provenance_list):
        provenances = []
        for entry in provenance_list:
            provenance = entry.get('Text')
            if provenance:
                datings = entry.get('Notes')
                datings_str = "{}: ".format(datings) if datings else ''
                provenances.append("{}{}".format(datings_str, provenance))
        return self.comma_separated(provenances)

    def get_geographic_location(self, keywords_list):
        for keyword in keywords_list:
            if keyword.get('Type') == 'Geogr. Bezug':
                text = keyword.get('Text')
                try:
                    return text.split('(')[0].strip()
                except IndexError:
                    return ''
        return ''

    def get_series_id(self, object_data):
        if len(object_data.get('OtherObjects')) > 0:
            inv_no = object_data.get('InventoryNumber')
            if inv_no:
                parts = inv_no.split('-')
                if len(parts) >= 3:
                    # MetaHubXXX-YYYY-ZZZZ -> MetaHubXXX-YYYY denotes series
                    series = parts[0] + parts[1]
                    return series
                else:
                    print('Cannot extract series out of object {}'.format(inv_no))
                    return None
        return None

    def get_or_create_object_page(self, object_instance,
                                  update_title=False,
                                  update_intro=False,
                                  update_highlight_status=False):
        try:
            page = MetaHubObjectPage.objects.get(object=object_instance)

            if update_title and object_instance.title:
                oldslug = page.slug
                # print('old: {} {}'.format(page.title, page.slug))
                page.title = object_instance.title
                page.slug = slugify(object_instance.title)
                # print('updating title and slug for page')
                try:
                    page.save()
                except:
                    page.slug = oldslug
                    page.save()
                    # print('duplicate slug for {}'.format(page.title))

            # Update intro text
            if update_intro:
                page.intro = object_instance.bc_notes
                page.save()

            # Get highlight status, was not there before
            if update_highlight_status:
                page.is_highlight = object_instance.is_highlight
                page.save()

            return page

        except MetaHubObjectPage.DoesNotExist:
            parent_page = MetaHubCategoryOverviewPage.objects.get(overview_category='object')
            new_page = MetaHubObjectPage(title=object_instance.title,
                                     collection_category=self.get_or_create_category('Objekt'),
                                     object=object_instance,
                                     )
            parent_page.add_child(instance=new_page)
            return new_page

    def get_or_create_series_page(self, object_instance):
        series_id = object_instance.series_id

        try:
            return MetaHubObjectSeriesPage.objects.get(series_id=series_id)
        except MetaHubObjectSeriesPage.DoesNotExist:
            parent_page = MetaHubCategoryOverviewPage.objects.get(overview_category='object_series')
            new_series_page = MetaHubObjectSeriesPage(
                title='Series {}'.format(series_id),
                collection_category=self.get_or_create_category('Objektserie'),
                series_id=series_id
            )
            parent_page.add_child(instance=new_series_page)
            return new_series_page

    def add_object_to_series_page(self, object_instance):
        page = self.get_or_create_series_page(object_instance)
        object_instance.series_page = page
        object_instance.save()
        page.save() # adding tags?



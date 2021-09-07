import json
import logging
import os
import zipfile

from django.core.management import BaseCommand
from django.utils.text import slugify

from metahub.collection.models import (
    BaseCollectionObject,
    BaseTag,
    MetaHubObjectPage,
    ObjectImageLink,
)
from metahub.home.models import MetaHubMuseumSubHomePage
from metahub.overviews.models import MetaHubOverviewPage
from metahub.sync.mapping.importer import amf, jmf, hmf
from metahub.sync.mapping.sync import BeeCollectMapping
from metahub.sync.models import BeeCollectSyncOccurrence
from metahub.sync.utils import add_fabrique_image

logger = logging.getLogger(__name__)

MUSEUMS = [
#    "amf",
    "hmf",
#    "jmf",
]
MUSEUM_ZIPFILES = {
#    "amf": "AMF_MetaHubExport.zip",
    "hmf": "HMF_MetaHubExport.zip",
#    "jmf": "JMF_MetaHubExport.zip",
}
MUSEUM_OBJECT_MAPPING = {
    "amf": amf.Object,
    "hmf": hmf.Object,
    "jmf": jmf.Object,
}


class Command(BaseCommand):
    help = """Imports the json with beecollect data from the specified path.
    The _data.json files need to be cleaned by the following bash script:
    `tr '}' '}\\n' < _data.json > cleaned_data.json`
    or
    `tr ',' ',\\n' < _data.json > cleaned_data.json`
    """

    def add_arguments(self, parser):
        parser.add_argument("beecollect_folder", nargs=1, type=str)
        parser.add_argument("sync_folder", nargs=1, type=str)

    def handle(self, beecollect_folder, sync_folder, *args, **options):
        BeecollectImporter().start(beecollect_folder[0], sync_folder[0])


class BeecollectImporter:
    def start(self, beecollect_folder, sync_folder):
        if not beecollect_folder.startswith("/"):
            logger.error("Path parameters need to be absolute paths, start with /")
            exit(1)
        if not sync_folder.startswith("/"):
            logger.error("Path parameters need to be absolute paths, start with /")
            exit(1)

        # we are remaking all links
        ObjectImageLink.objects.all().delete()
        update_title = True
        update_intro = True

        for museum in MUSEUMS:
            logger.info(f"*** Start Beecollect sync for {museum}")
            museum_sync_folder = os.path.join(sync_folder, museum)

            logger.info(f"Clearing old Beecollect data of {museum}")
            for filename in os.listdir(os.path.join(museum_sync_folder)):
                os.remove(os.path.join(museum_sync_folder, filename))

            logger.info(f"Unpacking Beecollect data of {museum}")
            with zipfile.ZipFile(os.path.join(beecollect_folder, MUSEUM_ZIPFILES[museum]), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(museum_sync_folder))

            logger.info(f"Importing {museum}")
            objects_added = 0
            objects_changed = 0
            objects_removed = 0

            ## Add artist here
            artist_data = self.get_items_from_file(museum_sync_folder, 'Artists')
            bcm = BeeCollectMapping(artist_data)
            for bc_a in artist_data:
                a = bcm.get_or_create_artist(bc_a)

            for object in self.get_items_from_file(museum_sync_folder, "Objects"):
                print(object)
                try:
                    obj = MUSEUM_OBJECT_MAPPING[museum](**object)
                except Exception as e:
                    logger.error(f"Import error '{museum}' for object id: {object['Id']}, {e}")
                    continue
                if not obj.Images:
                    logger.debug(
                        f"Skipping object '{obj.Id}' because there are no images present"
                    )
                    continue

                bco = BaseCollectionObject.objects.filter(bc_id=obj.Id)
                if bco:
                    bco.update(**obj.to_bc_dict())
                    bc_obj = bco.first()
                    logger.debug(f"Updating object '{obj.Id}' with id: {bc_obj.id}")
                    objects_changed += 1
                else:
                    bc_obj = BaseCollectionObject.objects.create(**obj.to_bc_dict())
                    logger.debug(f"Creating object '{obj.Id}' with id: {bc_obj.id}")
                    objects_added += 1

                #connect artist here



                for image in obj.Images:
                    if image.KeyFileName:
                        image_path = os.path.join(museum_sync_folder, image.KeyFileName)
                        try:
                            img = add_fabrique_image(
                                image_path,
                                overwrite=True,
                                attribution=image.License,
                                alt_text=obj.get_title(),
                            )
                            logger.debug(
                                f"Import image '{img.filename}' for object id: {bc_obj.id}"
                            )
                        except FileNotFoundError:
                            logger.warning(f"Image '{image_path}' not found for object: {obj.Id}")
                        else:
                            # Link with object-image-link
                            ObjectImageLink.objects.create(
                                object_image=img, collection_object=bc_obj
                            )

                for tag in obj.get_tags():
                    BaseTag.objects.get_or_create(name=tag)
                    logger.debug(f"Import tag '{tag}' for object id: {bc_obj.id}")

                self.get_or_create_object_page(
                    bc_obj, museum, update_title=update_title, update_intro=update_intro
                )

            BeeCollectSyncOccurrence.objects.create(
                museum=museum,
                date_data_dump=self.data.get("ExportDate"),
                objects_in_dump=self.data.get("NumberOfObjects"),
                objects_added=objects_added,
                objects_changed=objects_changed,
                objects_removed=objects_removed,
                success=True,
            )

    def get_or_create_object_page(
        self, object_instance, museum_slug, update_title=False, update_intro=False
    ):
        try:
            page = MetaHubObjectPage.objects.get(object=object_instance)

            if update_title:
                title = object_instance.title
                if not title:
                    title = object_instance.bc_id

                oldslug = page.slug
                # print('old: {} {}'.format(page.title, page.slug))
                page.title = title
                page.slug = slugify(title)
                # print('updating title and slug for page')
                try:
                    page.save()
                    logger.debug(
                        f"Updating CMS page for object id: {object_instance.id}"
                    )
                except:
                    page.slug = oldslug
                    page.save()
                    # print('duplicate slug for {}'.format(page.title))

            # Update intro text
            if update_intro:
                page.introduction = object_instance.bc_notes
                page.save()

            return page

        except MetaHubObjectPage.DoesNotExist:
            title = object_instance.title
            if not title:
                title = object_instance.bc_id
            logger.debug(f"Creating CMS page for object id: {object_instance.id}")
            # TODO Determine type (objects) (this might be german later on? its not super safe to do this by slug perhaps)
            parent_page = (
                MetaHubOverviewPage.objects.filter(slug="objects")
                .descendant_of(MetaHubMuseumSubHomePage.objects.get(slug=museum_slug))
                .first()
            )
            new_page = MetaHubObjectPage(title=title, object=object_instance)

            if not parent_page:
                logger.warning("Missing objects parent page to append children! Cannot continue.")

            parent_page.add_child(instance=new_page)
            return new_page
            # logger.warning(f"Can't create CMS page for object id: {object_instance.id}")


    def get_items_from_file(self, folder, items_section):
        """Parse the file line by line and yield everytime a full item is found.
        It's important that the input file has newlines, ideally after each closing curly bracket }
        """
        if items_section not in ["Objects", "Artists"]:
            return

        # TODO the code below is better for memory consumption to load huge _data.json files
        #  but it doesn't load the metadata (ExportDate, NumberOfObjects)
        # with open(os.path.join(folder, "cleaned_data.json"), "r") as fp:
        #     item = []
        #     in_items = False
        #     curly = 0
        #     brackets = 0
        #     for line in fp:
        #         if items_section in line:
        #             in_items = True
        #         if in_items:
        #             if "]" in line:
        #                 brackets -= 1
        #             if "[" in line:
        #                 brackets += 1
        #             if brackets == 0:
        #                 in_items = False
        #             if "}" in line:
        #                 curly -= 1
        #                 if curly == 0:
        #                     _line = "".join(item).strip(",") + "}"
        #                     item = []
        #                     object = json.loads(_line)
        #                     logger.debug(f"Import object '{object.get('Id')}'")
        #                     # logger.debug(_line)
        #                     yield object
        #                     logger.debug("---")
        #             if "{" in line:
        #                 curly += 1
        #             if curly > 0:
        #                 item.append(line.strip().replace("\n", ""))
        with open(os.path.join(folder, "_data.json"), "r") as fp:
            self.data = json.load(fp)
            for object in self.data.get(items_section):
                logger.debug(f"Import object '{object.get('Id')}'")
                yield object
                logger.debug("---")

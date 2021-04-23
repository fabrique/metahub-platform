import os
import json

from django.core.exceptions import MultipleObjectsReturned
from django.core.management import BaseCommand
from wagtail.core.models import Page

from metahub.collection.models import *
from metahub.core.models import MetaHubObjectPage, metahubImage, MetaHubObjectSeriesPage
from metahub.sync.mapping import BeeCollectMapping
from metahub.sync.utils import add_fabrique_image


class Command(BaseCommand):
    help = 'Imports the json with beecollect data from the specified path (sync next to the src folder)'

    def handle(self, *args, **options):

        #cleanup double images
        DOUBLE_IMG_CLEAN = False
        if DOUBLE_IMG_CLEAN:
            imgs = metahubImage.objects.all()
            for i in imgs:
                try:
                    mytest = metahubImage.objects.get(title=i.title)
                except MultipleObjectsReturned:
                    print('multiple for', i.title)
                    print('{} found'.format(len(metahubImage.objects.filter(title=i.title))))
                    double = metahubImage.objects.filter(title=i.title)[1]
                    double.delete()

            return 'done'


        # BaseCollectionObject.objects.all().delete()
        # BaseCollectionArtist.objects.all().delete()
        # metahubImage.objects.all().delete()
        # MetaHubObjectPage.objects.all().delete()
        # MetaHubObjectSeriesPage.objects.all().delete()

        # we are remaking all links
        ObjectImageLink.objects.all().delete()
        update_title = True
        sync_objects = True
        update_intro = True
        update_highlight_status = True

        with open('sync/_data.json', 'r') as data_string:  # MKR: changed path outside of repo
            data = json.load(data_string)
            bcm = BeeCollectMapping(data)

            if sync_objects:
                # Artists first, so objects can be linked to it
                for bc_a in data.get('Artists'):
                    a = bcm.get_or_create_artist(bc_a)

                    # Modification present
                    if bc_a.get('ChangeDate') != a.bc_change_date:
                        bcm.get_or_create_artist(bc_a, update=True)

                # Now that artists exist we can create the objects
                for bc_o in data.get('Objects'):
                    # Skip with no img for now
                    if len(bc_o.get('Images')) == 0:
                        #TODO: default image?
                        continue

                    object_instance = bcm.get_or_create_object(bc_o, update=True) # MKR: for now always update, later maybe only changed items.
                    # If it has changed, update
                    # if bc_o.get('ChangeDate') != object_instance.bc_change_date:
                    #     bcm.get_or_create_object(bc_o, update=True)

                    bcm.add_object_images(bc_o, object_instance)
                    bcm.add_tags_to_object(bc_o, object_instance)

        # Build the pages
        for object_instance in BaseCollectionObject.objects.all():
            # if object_instance.pk != 1379:
            #     continue
            page = bcm.get_or_create_object_page(object_instance,
                                                 update_title=update_title,
                                                 update_intro=update_intro,
                                                 update_highlight_status=update_highlight_status)

            if object_instance.series_id:
                bcm.add_object_to_series_page(object_instance)

        bcm.create_final_log()
        print(len(BaseCollectionObject.objects.all()))


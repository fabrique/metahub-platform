import json
import zipfile
from io import BytesIO

from django.db import models
from django.http import JsonResponse, HttpResponse
from starling.utils import render, if2context
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from metahub.collection.models.object_page import MetaHubObjectPage
# from metahub.collection.models.object_series_page import MetaHubObjectSeriesPage
from metahub.core.models import MetaHubBasePage
from metahub.stories.models.story_page import MetaHubStoryPage


class MetaHubMyCollectionPage(RoutablePageMixin, MetaHubBasePage):
    """
    Simple page that allows users to see an overview of their favourite items of
    the collection. Also has a possibility to allow a bulk download of the contents.
    Favourites are stored on the user's device through cookies, not in our DB.
    """

    # parent_page_types = []
    #
    # allow_download = models.BooleanField(default=True)
    #
    # content_panels = MetaHubBasePage.content_panels + [
    #     FieldPanel('title'),
    #     FieldPanel('allow_download')
    # ]
    #
    # def get_all_favourites(self, favourites):
    #     cards = []
    #
    #     objects = favourites.get('object', [])
    #     for o in objects:
    #         try:
    #             page = MetaHubObjectPage.objects.live().get(pk=o)
    #         except MetaHubObjectPage.DoesNotExist:
    #             pass # Fav specifies page that is not existing, skip
    #         else:
    #             interface = page.get_object_card_representation(classes='my-collection__object-card')
    #             html = render('molecules.object-card.regular', if2context(interface))
    #             cards.append(html)
    #
    #     series = favourites.get('series', [])
    #     for s in series:
    #         try:
    #             page = MetaHubObjectSeriesPage.objects.live().get(pk=s)
    #         except MetaHubObjectSeriesPage.DoesNotExist:
    #             pass  # Fav specifies page that is not existing, skip
    #         else:
    #             interface = page.get_object_card_representation(classes='my-collection__object-card')
    #             html = render('molecules.object-card.regular', if2context(interface))
    #             cards.append(html)
    #
    #     stories = favourites.get('story', [])
    #     for s in stories:
    #         try:
    #             page = MetaHubStoryPage.objects.live().get(pk=s)
    #         except MetaHubStoryPage.DoesNotExist:
    #             pass # Fav specifies page that is not existing, skip
    #         else:
    #             interface = page.get_card_representation(classes='my-collection__card')
    #             html = render('molecules.card.regular', if2context(interface))
    #             cards.append(html)
    #
    #     return cards
    #
    # def get_download_info(self):
    #     if self.allow_download:
    #         return {
    #             'href' : self.url + 'download',
    #             'title': 'Alle Bilder downloaden',
    #         }
    #     else:
    #         return None
    #
    # def get_all_images(self, favourites):
    #     """
    #     Retrieves the images that belong to the objects and object series
    #     in the favourites. Stories are omitted as they often contain
    #     copyrighted imagery.
    #     """
    #     images = []
    #
    #     objects = favourites.get('object', [])
    #     for o in objects:
    #         try:
    #             page = MetaHubObjectPage.objects.live().get(pk=o)
    #         except MetaHubObjectPage.DoesNotExist:
    #             pass # Fav specifies page that is not existing, skip
    #         else:
    #             images += page.get_raw_images()
    #
    #     series = favourites.get('series', [])
    #     for s in series:
    #         try:
    #             page = MetaHubObjectSeriesPage.objects.live().get(pk=s)
    #         except MetaHubObjectSeriesPage.DoesNotExist:
    #             pass  # Fav specifies page that is not existing, skip
    #         else:
    #             images += page.get_raw_images()
    #
    #     return images
    #
    # def generate_zip(self, files_list):
    #     """
    #     Add the files to the zip in memory.
    #     """
    #     mem_zip = BytesIO()
    #
    #     with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
    #         for f in files_list:
    #             zf.writestr(f[0], f[1])
    #
    #     return mem_zip.getvalue()
    #
    # @route(r'^get_favourites/')
    # def get_favourites(self, request, *args, **kwargs):
    #     """
    #     Returns html to be inserted in the page.
    #     """
    #     favourites = request.GET.get('data')
    #     cards = []
    #     if favourites:
    #         favourites_str = json.loads(favourites)
    #         favourites_dict = json.loads(favourites_str)
    #         cards = self.get_all_favourites(favourites_dict)
    #
    #         # Store in session so we can use it for download
    #         request.session['favourites'] = favourites_dict
    #
    #     return JsonResponse(cards, safe=False)
    #
    # @route(r'^download/')
    # def download(self, request, *args, **kwargs):
    #     """
    #     Returns a .zip file with all downloaded files.
    #     """
    #     favourites = request.session['favourites']
    #     if favourites:
    #         images = self.get_all_images(favourites)
    #
    #         files_list = []
    #         for image in images:
    #             try:
    #                 path = image.file.path
    #             except AttributeError:
    #                 pass
    #             else:
    #                 file = open(path, "rb")
    #                 files_list.append((str(image), file.read()))
    #                 file.close()
    #
    #         zip_file = self.generate_zip(files_list)
    #         response = HttpResponse(zip_file, content_type='application/force-download')
    #         response['Content-Disposition'] = 'attachment; filename="%s"' % 'mein-sammlung.zip'
    #         return response
    #
    #     return Page.serve(self, request, *args)
    #
    # @route(r'^$')
    # def regular_landing(self, request, *args, **kwargs):
    #     return Page.serve(self, request, *args)
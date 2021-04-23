import json
import urllib.parse
import zipfile
from datetime import datetime
from io import BytesIO
from itertools import chain
from random import random, randint, choice as randomchoice

from django.core.paginator import PageNotAnInteger
from django.db import models
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea
from modelcluster.contrib.taggit import ClusterTaggableManager
from starling.interfaces.generic import Resolution
from starling.utils import render, if2context
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, TabbedInterface, StreamFieldPanel, MultiFieldPanel, \
    InlinePanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index

from .mixins import PagePromoMixin
from .utils import ReadOnlyPanel

from pure_pagination import Paginator

from ..collection.models import BaseCollectionObject, BaseCollectionArtist, CollectionObjectTag, \
    CollectionObjectSeriesTag

from ..starling_metahub.molecules.blocks import MoleculeAudioPlayerBlock
from ..starling_metahub.molecules.interfaces import MoleculeContextCardRegular, MoleculeObjectCardRegular
from ..starling_metahub.organisms.blocks import OrganismHeroHeaderMultiImageRegularBlock, \
    OrganismContentSingleRichTextRegularBlock, \
    OrganismContentSingleImageRegularBlock, OrganismContentSingleVideoRegularBlock, \
    OrganismContentDoubleQuoteRichTextRegularBlock, OrganismContentDoubleImageRichTextRegularBlock, \
    OrganismObjectMosaicChoiceRegularBlock, OrganismContextDiscoveryChoiceRegularBlock, OrganismLinkListRegularBlock, \
    AtomPictureRegular, OrganismContentSingleAudioRegularBlock, OrganismSearchHeaderRegularBlock, \
    OrganismThemeHighlightsRegularBlock, OrganismObjectHighlightsRegularBlock, OrganismCollectionCategoriesRegularBlock, \
    OrganismHeroHeaderSingleImageContentPageRegularBlock, OrganismArticleCookieBlockRegular
from ..starling_metahub.organisms.interfaces import OrganismImageIntroRegular, OrganismHeroHeaderMultiImageRegular, \
    OrganismObjectHighlightsRegular, OrganismThemeHighlightsRegular, OrganismRelatedItemsRegular
from ..starling_metahub.structures.blocks import StructureFooterBarSimpleBlock


class metahubBasePage(PagePromoMixin, Page):
    """
    Base page for all MetaHub online collection pages
    """
    def get_my_collection_url(self):
        my_collection = MetaHubMyCollectionPage.objects.live().first()
        if my_collection:
            return my_collection.url
        return '/'

    def get_search_base_url(self):
        """
        Used by the tags that redirect to search with a predefined param
        as well as the object series "see all objects in this series"
        """
        search =  MetaHubSearchPage.objects.live().first()
        if search:
            return search.search_url()
        return '/'

    def get_highlights(self):
        """
        Checks for each page type what pages have been marked as
        highlights and creates a card representation to show.
        """
        cards = []
        obj_highlights = MetaHubObjectPage.objects.all().specific().live().filter(is_highlight=True)
        obj_series_highlights = MetaHubObjectSeriesPage.objects.all().specific().live().filter(is_highlight=True)
        story_highlights = MetaHubStoryPage.objects.all().specific().live().filter(is_highlight=True)

        all_highlights = list(chain(obj_highlights, obj_series_highlights, story_highlights))

        for highlight in all_highlights:
            cards.append(highlight.get_search_representation())

        return cards

    class Meta:
        abstract = True


class MetaHubContentPage(metahubBasePage):
    hero_header = StreamField([
        ('header_image', OrganismHeroHeaderSingleImageContentPageRegularBlock()),
    ])

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('single_image', OrganismContentSingleImageRegularBlock()),
        ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('cookies', OrganismArticleCookieBlockRegular())
    ])

    content_panels = metahubBasePage.content_panels + [
        StreamFieldPanel('hero_header'),
        StreamFieldPanel('content')
    ]

class MetaHubSearchPage(RoutablePageMixin, metahubBasePage):
    """
    Page with search header that supports live search on top, and filters below.
    Results are rendered on a card grid and refreshed using AJAX.
    """
    search_header = StreamField([
        ('search_header', OrganismSearchHeaderRegularBlock())
    ])

    content_panels = metahubBasePage.content_panels + [
        StreamFieldPanel('search_header'),
    ]

    def get_random_header_picture(self):
        """
        Picks one of the chosen header images.
        """
        try:
            header_child = self.search_header[0]
        except IndexError:
            return None
        else:
            picture_structvalues = header_child.value['pictures']
            picture_index = randint(0, len(picture_structvalues) - 1)
            return picture_index

    def search_view(self, request, *args, **kwargs):
        """
        Used by the AJAX request done on the search landing so that not all
        the page refreshes but only the results/cards at the bottom.
        """
        context = self.get_context(request, *args, **kwargs)
        content = render_to_string('core/components/search_filter_results.html', context=context)
        output = {}
        output['content'] = content
        return JsonResponse(data=output, safe=False)

    def live_search_url(self):
        return self.url + self.reverse_subpage('livesearch_landing')

    def search_url(self):
        return self.url + self.reverse_subpage('regular_landing')

    @route(r'^live/')
    def livesearch_landing(self, request, *args, **kwargs):
        """
        Used to determine and render the livesearch results. Stringifies the template
        so frontend can render it as is immediately.
        """

        # Required to avoid circular imports
        from ..collection.search import do_search

        query = request.GET.get('search')
        context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)

        # Get first 5 results and output the template for the livesearch bar
        context['results'] = do_search(query)[:5]
        content = render_to_string('core/components/search_bar_result.html', context=context)
        output = {}
        output['content'] = content
        return JsonResponse(data=output, safe=False)

    @route(r'^$')
    def regular_landing(self, request, *args, **kwargs):
        """
        Landing with header on top and search results at the bottom. Initially
        loads all results if no params are given, subsequent search operations
        are handled by AJAX.
        """
        if request.is_ajax():
            return self.search_view(request, *args, **kwargs)

        return Page.serve(self, request, *args, **kwargs)

    def get_active_filters(self, request):
        """
        Reconstructs filters according to the current situation. Since this also affects
        the available result count we use the facets from ES again.
        """
        get_vars = request.GET

        # Check this list of facet filters
        str_facets = ['artist', 'material', 'tags', 'object_category', 'provenance', 'type', 'series', 'is_highlight']
        af = {}
        for f in str_facets:
            value = get_vars.get('id_{}'.format(f))
            if value:
                af[f] = value

        # We need to reconstruct the date object, actually no, since we do a range query by hand
        # TODO: Does urllib.parse need a safety try/catch?
        # date_facets = ['dating_from', 'dating_to']
        # for f in date_facets:
        #     value = get_vars.get('id_{}'.format(f))
        #
        #     if value:
        #         date_str = urllib.parse.unquote(value)
        #         date_str = "{}-1-1".format(date_str)
        #         try:
        #             date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        #         except ValueError:
        #             pass # Date was not in right format in url, skip it
        #         else:
        #             af[f] = date_obj
        return af

    def get_context(self, request, *args, **kwargs):
        # Required to avoid circular imports
        from ..collection.search import get_search_results, get_result_as_cards, get_result_filters

        context = super(MetaHubSearchPage, self).get_context(request, *args, **kwargs)
        search_string = request.GET.get('search')
        applied_filters = self.get_active_filters(request)
        search_results = get_search_results(search_string, applied_filters, request.GET)

        # Try to parse the results, if there are none use highlights
        search_results_cards = get_result_as_cards(search_results)

        if len(search_results_cards) == 0:
            search_results_cards = self.get_highlights()
            context['no_results'] = True

        context['filters'] = get_result_filters(search_results, request.GET)

        # Pagination for found objects
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(search_results_cards, request=request, per_page=12)
        paginator_page = paginator.page(page)

        context.update({
            'results': paginator_page.object_list,
            'paginator': paginator_page,
            'search_filters' : applied_filters,
            'search_query' : search_string
        })

        context['result_count'] = '{} Resultate'.format(len(search_results))
        return context


class MetaHubHomePage(RoutablePageMixin, metahubBasePage):
    """
    Homepage of the collection website. Features a header that supports livesearch, but
    directs user to search result when executing actual query. Other content includes a
    set of highlighted stories, objects and an overview of the collection categories.
    """
    search_header = StreamField([
        ('search_header', OrganismSearchHeaderRegularBlock())
    ])

    theme_block = StreamField([
        ('theme_block', OrganismThemeHighlightsRegularBlock())
    ])

    highlights_block = StreamField([
        ('highlights_block', OrganismObjectHighlightsRegularBlock())
    ])

    collection_categories_block = StreamField([
        ('collection_categories_block', OrganismCollectionCategoriesRegularBlock())
    ])

    content_panels = metahubBasePage.content_panels + [
        StreamFieldPanel('search_header'),
        StreamFieldPanel('theme_block'),
        StreamFieldPanel('highlights_block'),
        StreamFieldPanel('collection_categories_block')
    ]

    def get_random_header_picture(self):
        """
        Picks one of the chosen header images.
        """
        try:
            header_child = self.search_header[0]
        except IndexError:
            return None
        else:
            picture_structvalues = header_child.value['pictures']
            picture_index = randint(0, len(picture_structvalues) - 1)
            return picture_index

    def get_context(self, request, *args, **kwargs):
        context = super(MetaHubHomePage, self).get_context(request, *args, **kwargs)
        searchpage = MetaHubSearchPage.objects.all().specific()
        if len(searchpage):
            context['searchpage'] = searchpage[0]
        return context

    def get_collection_themes(self):
        """
        Based on the themes/stories chosen, retrieve the content needed to render frontend
        from these stories.
        """
        themes = self.theme_block[0]
        theme_cards = []

        for element in themes.value['themes']:
            if element['page']:
                page = element['page'].specific

                if element['intro_text'] and len(element['intro_text']) != 0:
                    text = element['intro_text']
                else:
                    text = page.highlight_intro

                theme_cards.append({
                    'title': page.title,
                    'description': text,
                    'picture': page.get_primary_image(),
                    'background_images': page.get_hero_images()[1:],
                    'link': {
                                'href' : page.url,
                                'title': '',
                                'long_title': '',
                              }
                })

        theme_categories = []
        for element in themes.value['theme_categories']:
            theme_categories.append(element)

        data = OrganismThemeHighlightsRegular(
            title=themes.value['title'],
            subtitle=themes.value['subtitle'],
            theme_categories=theme_categories,
            themes=theme_cards
        )
        return data

    def get_object_highlights(self):
        """
        Objects of the collection that get the spotlight. A set of 5 objects is
        supported by the frontend. Since listblock does not seem to support
        min/max_num this is enforced here by slicing the list.
        """
        highlights = self.highlights_block[0]
        highlight_cards = []

        for element in highlights.value['highlights']:
            page = element['page'].specific

            # Check if the highlight has text
            text = element['intro_text'] if not None else page.highlight_intro

            # Get object
            object = None
            if isinstance(page, MetaHubObjectPage):
                object = page.object
            elif isinstance(page, MetaHubObjectSeriesPage):
                object = page.get_primary_object()

            # Build card (it does not use a molecule)
            highlight_cards.append({
                'href' : page.url,
                'description': text,
                'title' : page.title,
                'picture' : page.get_primary_image(),
                'detail' : page.get_object_artist(), # Page type is enforced by chooser block
                'subdetail': page.get_type_dating(),
                'location' : object.current_location,
            })

        # Build component as a whole
        return OrganismObjectHighlightsRegular(
            title=highlights.value['title'],
            introduction=highlights.value['introduction'],
            cards=highlight_cards[:5],
            all_highlights_url="{}?id_is_highlight=true".format(self.get_search_base_url())
        )


class MetaHubMyCollectionPage(RoutablePageMixin, metahubBasePage):
    """
    Simple page that allows users to see an overview of their favourite items of
    the collection. Also has a possibility to allow a bulk download of the contents.
    Favourites are stored on the user's device through cookies, not in our DB.
    """

    allow_download = models.BooleanField(default=True)

    content_panels = metahubBasePage.content_panels + [
        FieldPanel('title'),
        FieldPanel('allow_download')
    ]

    def get_all_favourites(self, favourites):
        cards = []

        objects = favourites.get('object', [])
        for o in objects:
            try:
                page = MetaHubObjectPage.objects.live().get(pk=o)
            except MetaHubObjectPage.DoesNotExist:
                pass # Fav specifies page that is not existing, skip
            else:
                interface = page.get_object_card_representation(classes='my-collection__object-card')
                html = render('molecules.object-card.regular', if2context(interface))
                cards.append(html)

        series = favourites.get('series', [])
        for s in series:
            try:
                page = MetaHubObjectSeriesPage.objects.live().get(pk=s)
            except MetaHubObjectSeriesPage.DoesNotExist:
                pass  # Fav specifies page that is not existing, skip
            else:
                interface = page.get_object_card_representation(classes='my-collection__object-card')
                html = render('molecules.object-card.regular', if2context(interface))
                cards.append(html)

        stories = favourites.get('story', [])
        for s in stories:
            try:
                page = MetaHubStoryPage.objects.live().get(pk=s)
            except MetaHubStoryPage.DoesNotExist:
                pass # Fav specifies page that is not existing, skip
            else:
                interface = page.get_card_representation(classes='my-collection__card')
                html = render('molecules.card.regular', if2context(interface))
                cards.append(html)

        return cards

    def get_download_info(self):
        if self.allow_download:
            return {
                'href' : self.url + 'download',
                'title': 'Alle Bilder downloaden',
            }
        else:
            return None

    def get_all_images(self, favourites):
        """
        Retrieves the images that belong to the objects and object series
        in the favourites. Stories are omitted as they often contain
        copyrighted imagery.
        """
        images = []

        objects = favourites.get('object', [])
        for o in objects:
            try:
                page = MetaHubObjectPage.objects.live().get(pk=o)
            except MetaHubObjectPage.DoesNotExist:
                pass # Fav specifies page that is not existing, skip
            else:
                images += page.get_raw_images()

        series = favourites.get('series', [])
        for s in series:
            try:
                page = MetaHubObjectSeriesPage.objects.live().get(pk=s)
            except MetaHubObjectSeriesPage.DoesNotExist:
                pass  # Fav specifies page that is not existing, skip
            else:
                images += page.get_raw_images()

        return images

    def generate_zip(self, files_list):
        """
        Add the files to the zip in memory.
        """
        mem_zip = BytesIO()

        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in files_list:
                zf.writestr(f[0], f[1])

        return mem_zip.getvalue()

    @route(r'^get_favourites/')
    def get_favourites(self, request, *args, **kwargs):
        """
        Returns html to be inserted in the page.
        """
        favourites = request.GET.get('data')
        cards = []
        if favourites:
            favourites_str = json.loads(favourites)
            favourites_dict = json.loads(favourites_str)
            cards = self.get_all_favourites(favourites_dict)

            # Store in session so we can use it for download
            request.session['favourites'] = favourites_dict

        return JsonResponse(cards, safe=False)

    @route(r'^download/')
    def download(self, request, *args, **kwargs):
        """
        Returns a .zip file with all downloaded files.
        """
        favourites = request.session['favourites']
        if favourites:
            images = self.get_all_images(favourites)

            files_list = []
            for image in images:
                try:
                    path = image.file.path
                except AttributeError:
                    pass
                else:
                    file = open(path, "rb")
                    files_list.append((str(image), file.read()))
                    file.close()

            zip_file = self.generate_zip(files_list)
            response = HttpResponse(zip_file, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'mein-sammlung.zip'
            return response

        return Page.serve(self, request, *args)

    @route(r'^$')
    def regular_landing(self, request, *args, **kwargs):
        return Page.serve(self, request, *args)


class AbstractMetaHubRichBasePage(metahubBasePage):

    class Meta:
        abstract = True

    # Dtefines the broader category of this page, for example "artwork" or "family legacy"
    collection_category = models.ForeignKey(
        'collection.CollectionCategory',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    is_highlight = models.BooleanField(blank=True, default=False)

    # Intro that is used on the homepage
    highlight_intro = models.TextField(max_length=4096, blank=True, default='')

    # Text of the introduction component
    intro = models.TextField(max_length=4096, blank=True)
    reading_time = models.PositiveIntegerField(default=0, null=True, blank=True)
    show_reading_time = models.BooleanField(default=False)
    audio = StreamField([('audio', MoleculeAudioPlayerBlock())], blank=True)

    # Main content block, differs per subclass
    content = StreamField([])

    # Cards at the bottom of the page, can be a link to a story or object
    discover_in_context = StreamField([
        ('card_list', OrganismContextDiscoveryChoiceRegularBlock())
    ], blank=True)

    content_panels = metahubBasePage.content_panels + [
        StreamFieldPanel('discover_in_context'),
        MultiFieldPanel([
            FieldPanel('is_highlight'),
            FieldPanel('highlight_intro')
        ]),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('show_reading_time'),
            StreamFieldPanel('audio')
        ], "Sub header")
    ]

    def get_category(self):
        """
        Stringified version of the page's category (Objekt, Geschichten, Series etc.)
        """
        try:
            return str(self.collection_category)
        except AttributeError:
            return ''

    def estimate_reading_time(self):
        if self.show_reading_time:
            word_count = 0

            for stream_child in self.content:
                try:
                    word_count += stream_child.block.get_word_count(stream_child.value)
                except AttributeError:
                    pass

            return str(1 + word_count // 200)

    def has_context(self):
        """
        Checks whether the context ribbon should be shown, based on if there is
        any context defined in the CMS. Passed on to the template to trigger
        correct layout.
        """
        try:
            self.discover_in_context[0]
        except IndexError:
            return False
        return True

    def build_context_cards(self):
        """
        If context cards were chosen, build the right ones. Each page defines its
        own method to render the correct card which we can use.
        """
        cards = []
        if self.has_context():
            organism_cards = self.discover_in_context[0]
            for card in organism_cards.value['cards']:
                if card['page']:
                    page = card['page'].specific
                    cards.append(page.get_card_representation())
            return cards[:3]
        else:
            return cards

    def build_intro(self):
        """
        Builds the correct intro component based on the type of hero component.
        Originally intended to support both video and image. At the moment the
        museum has no video content so this always returns the picture variant.
        """
        return self.build_picture_intro()

    def build_picture_intro(self):
        """
        Build the intro component based on the images that were uploaded into the
        hero image header.
        """
        pictures = self.get_hero_images()
        description = {'text': self.intro }
        component = OrganismImageIntroRegular(reading_time=self.reading_time,
                                              pictures=pictures,
                                              description=description,
                                              type='',
                                              audio=self.get_audio(),
                                              information=self.get_hero_info(),
                                              minimal=self.has_no_rich_content(),
                                              favinfo=self.get_favourite_info()
                                              )
        return component

    def has_no_rich_content(self):
        """
        Checks whether any non-automatically generated content is present. Determines
        whether the minimal layout variant should be triggered in template.
        """

        try:
            self.content[0]
        except IndexError:
            no_body_content = True
        else:
            no_body_content = False

        if not self.intro:
            no_intro_content = True
        else:
            no_intro_content = False

        return no_body_content and no_intro_content

    def get_audio(self):
        """
        The intro component supports an audio fragment. Takes the audio fragment
        from the CMS if any was chosen and returns this so the intro can use it.
        """
        try:
            audio_child = self.audio[0]
        except IndexError:
            return None
        else:
            return audio_child.block.build_component(audio_child.value)

    def get_lightbox_items(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_lightbox_items on the subclass')

    def get_search_representation(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_search_representation on the subclass')


    def get_card_representation(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_card_representation on the subclass')

    def build_hero_header(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement build_hero_header on the subclass')

    def get_hero_images(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_hero_images on the subclass')

    def get_hero_info(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_hero_info on the subclass')

    def get_primary_image(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_primary_image on the subclass')

    def get_raw_images(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_raw_image on the subclass')

    def get_tags_as_list(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_tags_as_list on the subclass')

    def get_favourite_info(self):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement get_favourite_info on the subclass')

    def is_favourite(self, request):
        """
        Needs to be overridden and implemented by subclass.
        """
        raise NotImplementedError('You need to implement is_favourite on the subclass')

    def get_promo_image(self):
        return self.get_primary_image()

    def save(self, *args, **kwargs):
        self.reading_time = self.estimate_reading_time()
        super().save(**kwargs)


class MetaHubObjectPage(AbstractMetaHubRichBasePage):
    """
    Page for the rich collection objects. It defines the object it is related to.
    Through this object we also gain access to the fields such as artist, object
    category etc. The users can add rich content to this page in the CMS.

    There are some read-only fields that allow the user to view this info in the CMS.
    This is probably not the best way to implement this but it does the job for now.

    This class overrides a lot of the methods from AbstractMetaHubRichBasePage. See the
    superclass for an overview of possible overrides.
    """

    # Page object
    object = models.ForeignKey(BaseCollectionObject, null=True, on_delete=models.SET_NULL, blank=True, related_name='associated_page')

    # Maximum of related objects shown
    MAX_RELATED_OBJECTS = 4

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('single_video', OrganismContentSingleVideoRegularBlock()),
        ('single_image', OrganismContentSingleImageRegularBlock()),
        ('single_audio', OrganismContentSingleAudioRegularBlock()),
        ('double_quote_richtext', OrganismContentDoubleQuoteRichTextRegularBlock()),
        ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
    ], blank=True)
    tags = ClusterTaggableManager(through=CollectionObjectTag, blank=True)

    content_panels = AbstractMetaHubRichBasePage.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('tags'),
        FieldPanel('object'),
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

    def build_hero_header(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Creates an image based hero header automatically (cannot be set in CMS) based
        on data from BeeCollect.
        """
        return OrganismHeroHeaderMultiImageRegular(
            information=self.get_hero_info(),
            expandable=True,
            pictures=self.get_object_images(),
            theme='white'
        )

    def get_hero_images(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        For this kind of page, images are not chosen in the CMS but are automatically
        retrieved from the corresponding object.
        """
        return self.get_object_images()

    def get_object_artist(self):
        if self.object:
            if self.object.artist:
                return str(self.object.artist)
            else:
                return 'Unbekannt'
        return None

    def get_type_dating(self):
        date = self.object.datings
        dating = ", {}".format(date) if date else ''

        type = self.object.object_type
        return "{}{}".format(type, dating)

    def get_hero_info(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Determines information that is displayed in this page type's hero header.
        """
        if self.get_object_artist():
            name = self.get_object_artist()
        else:
            name = self.get_category()


        return {
            'name': name,
            'title': self.title,
            'date': self.get_type_dating()
        }

    def get_tags(self):
        """
        Generates the frontend-compatible list of tags. These are the tags from the
        django-taggit model, and can be managed in the CMS.
        """
        if self.tags and len(self.tags.all()) > 0:
            searchpage = self.get_search_base_url()
            tags = { 'title' : 'Schlagworte', 'tag_items' : [ {'title': str(tag), 'href': '{}?id_tags={}'.format(searchpage, str(tag)) } for tag in self.tags.all()] }
            return tags
        return None

    def get_api_tags(self):
        """
        Generates the API-compatible list of tags. These are the tags from the
        django-taggit model, and can be managed in the CMS.
        """
        if self.tags and len(self.tags.all()) > 0:
            tags = [{'title': str(tag), 'href': '/search?id_tags={}'.format(str(tag)) } for tag in self.tags.all()]
            return tags
        return []

    def get_tags_as_list(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Used for ES indexing. At the moment stories do not have tags, but
        this might be added in the future.
        """
        return [str(tag) for tag in self.tags.all()]

    def get_search_representation(self):
        """
        Renders card for search result views.
        """
        return self.get_object_card_representation()

    def get_card_representation(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Decides what info to present on the "Discover collection in context" card.
        This card format also exist for stories, in a different color.
        """
        return MoleculeContextCardRegular(
            href=self.url,
            color='white',
            title=self.get_hero_info()['title'],
            type=self.get_category(),
            picture=self.get_primary_image()
        )

    def get_primary_image(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Image that is used if representing the object in a card or other component.
        TODO: return a default image if not found (objects without image can exist)
        """
        images = self.get_object_images()
        if images:
            return images[0]
        # Return default image
        else:
            return None

    def get_raw_images(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Used when we need the raw images and not the atomized variant.
        """
        if self.object:
           if self.object.bc_image_license:
               #no copyrighted images!
               if self.object.bc_image_license.find('©') != -1 or self.object.bc_image_license.find('(c)') != -1:
                   return []
           image_links = self.object.obj_img_link.all()
           return [link.object_image for link in image_links]
        return []

    def get_object_card_representation(self, classes=''):
        """
        Object specific card representation, for example for the "related" objects
        component. Search results are based on this template as well but not called from
        here but based on indexed data.
        """
        return MoleculeObjectCardRegular(
            href=self.url,
            title=self.get_hero_info()['title'],
            name=self.get_hero_info()['name'],
            picture=self.get_primary_image(),
            type=self.get_category(),
            date=self.object.datings,
            classes=classes,
        )

    def get_lightbox_items(self):
        """
        Get lightbox items and information. Since we need access to the properties
        of the MetaHubImage object we can't reuse get_object_images for this.
        """
        data = []
        if self.object:
           image_links = self.object.obj_img_link.all()
           for image_link in image_links:
               image = image_link.object_image
               image_data = {
                   'picture' : AtomPictureRegular(**Resolution(mobile='2048', landscape='4096', crop=True).resolve(image)),
                   'information': {
                       'title' : self.title,
                       'name' : self.get_object_artist(),
                       'description': '', #image.alt_text, #MKR this is wrong, but what else to show here?
                       'credits': image.attribution,
                   }
               }
               data.append(image_data)
        return data

    def get_object_images(self):
        """
        Retrieve all images belonging to this page's linked object and transform them
        into a frontend component. Can be passed to heroimage/slideshow components.
        """
        if self.object:
           images = self.object.obj_img_link.all()
           return [AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image.object_image)) for image in
                    images]
        return []

    def build_metadata(self):
        """
        Creates the right format that the frontend accepts for the object metadata fields.
        The information displayed here is based on BeeCollect data and not managable in the
        CMS, though it can be viewed in the metadata tab.
        TODO: Support localization , lol
        """
        if self.object:
            return [
                {
                    'title': 'Basisdaten',
                    'information': self.object.get_metadata_information_fields()
                },
                {
                    'title' : 'Eigentum und Erwerbung',
                    'information' : self.object.get_metadata_property_inheritance_fields()
                },
                {
                    'title': 'Ausstellungen',
                    'information': self.object.get_metadata_display_fields()
                }
            ]
        else:
            return []

    def build_related_objects(self):
        """
        Determine what objects should be shown in the related objects component.
        Maximum of 4. Checks for: same artist, same tags, same material, same category.
        """
        no_related_found = False
        page_pool = MetaHubObjectPage.objects.live().exclude(pk=self.pk)

        # First check for the same artist, if it has one
        related_pages = []

        if self.object.artist:
            results = page_pool.distinct().filter(object__artist=self.object.artist,
                                       object__object_type=self.object.object_type,
                                       tags__name__in=self.tags.all())
        else:
            results = page_pool.distinct().filter(object__object_type=self.object.object_type,
                                       tags__name__in=self.tags.all())

        # Nothing found, use random?
        if len(results) == 0:
            results = page_pool.distinct()
            no_related_found = True

        # Get random 4 objects
        tries = 0
        while tries < 100 and len(related_pages) < 4:
            new_page = randomchoice(results)
            if new_page not in related_pages:
                related_pages.append(new_page)
            tries += 1

        # Fill up with the rest if nothing found or too many tries
        if len(related_pages) < 4:
            needed = len(related_pages) - 4
            existing = [p.pk for p in related_pages]
            others = page_pool.distinct().exclude(pk__in=existing)

            # Append random objects
            if others:
                tries = 0
                while tries < 100 and len(related_pages) < 4:
                    new_page = randomchoice(others)
                    if new_page not in related_pages:
                        related_pages.append(new_page)
                    tries += 1

                # Not strictly related anymore
                no_related_found = True

        cards = []
        for related_page in related_pages:
            cards.append(related_page.get_object_card_representation())

        return OrganismRelatedItemsRegular(
            title='Andere Objekte' if no_related_found else 'Verwandte Objekte',
            related_objects=cards
            )


    def get_favourite_info(self):
        """
        Specifies category and unique idenfifier for this page.
        """
        return {
            'category' : 'object',
            'id': self.pk,
        }

    def save(self, *args, **kwargs):
        super().save(**kwargs)

        # If saving for the first time after creation,
        # add tags from the BeeCollect object to django-taggit
        # MKR , maybe also when not saving for the first time...

        if self.pk:
            # not foolproof in checking, but for now fine, so the only way to add tags is from beecollect! otherwise no way to tell changes
            if len(self.object.get_bc_tags_as_list()) != len(self.tags.all()):
                for t in self.tags.all():
                    t.delete()
            if len(self.tags.all()) == 0:
                self.tags.set(*self.object.get_bc_tags_as_list())
            super().save(**kwargs)

    def get_context(self, request, *args, **kwargs):
        # Required to avoid circular imports
        context = super(MetaHubObjectPage, self).get_context(request, *args, **kwargs)
        context['bc'] = request.GET.get('c','')  #bodyclass for testing
        return context


class MetaHubObjectSeriesPage(AbstractMetaHubRichBasePage):
    """
    Page that represents a series of objects. Objects can be defined to belong to one
    series at a time. For some objects this is done automatically upon import from
    BeeCollect. Just like with the MetaHubObjectPage users can add rich content.

    This class overrides a lot of the methods from AbstractMetaHubRichBasePage. See the
    superclass for an overview of possible overrides.
    """

    # In case the series is defined through BeeCollect
    series_id = models.CharField(max_length=256, default=None, blank=True, null=True)

    # Amount of objects shown in the grid before "show more" appears
    MAX_SHOWN_OBJECTS = 6

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('single_video', OrganismContentSingleVideoRegularBlock()),
        ('single_image', OrganismContentSingleImageRegularBlock()),
        ('single_audio', OrganismContentSingleAudioRegularBlock()),
        ('double_quote_richtext', OrganismContentDoubleQuoteRichTextRegularBlock()),
        ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('objects_choice', OrganismObjectMosaicChoiceRegularBlock())
    ], blank=True)
    tags = ClusterTaggableManager(through=CollectionObjectSeriesTag, blank=True)

    content_panels = AbstractMetaHubRichBasePage.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('tags')
    ]

    def build_hero_header(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Creates an image based hero header automatically (cannot be set in CMS) based
        on the first image of every object in the series.
        """
        return OrganismHeroHeaderMultiImageRegular(
            information=self.get_hero_info(),
            expandable=True,
            pictures=self.get_object_images(),
            theme='white'
        )

    def get_lightbox_items(self):
        """
        Get lightbox items and information. Since we need access to the properties
        of the MetaHubImage object we can't reuse get_object_images for this.
        """
        data = []
        for object in self.get_associated_objects():
           image_links = object.obj_img_link.all()
           for image_link in image_links:
               image = image_link.object_image
               image_data = {
                   'picture' : AtomPictureRegular(**Resolution(mobile='2048', landscape='4096', crop=True).resolve(image)),
                   'information': {
                       'title' : self.title,
                       'name' : self.get_object_artist(),
                       'description': '',
                       'credits': image.attribution,
                   }
               }
               data.append(image_data)
        return data


    def get_hero_images(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        For this kind of page, images are not chosen in the CMS but are automatically
        retrieved from the corresponding object.
        """
        return self.get_object_images()

    def get_hero_info(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Determines information that is displayed in this page type's hero header.
        """
        return {
            'name': self.get_category(),
            'title': self.title,
        }

    def get_tags(self):
        """
        Generates the frontend-compatible list of tags. These are the tags from the
        django-taggit model, and can be managed in the CMS.
        """
        if self.tags and len(self.tags.all()) > 0:
            searchpage = self.get_search_base_url()
            tags = {'title': 'Schlagworte', 'tag_items': [{'title': str(tag), 'href': '{}?id_tags={}'.format(searchpage, str(tag)) } for tag in self.tags.all()]}
            return tags
        return None

    def get_api_tags(self):
        """
        Generates the API-compatible list of tags. These are the tags from the
        django-taggit model, and can be managed in the CMS.
        """
        if self.tags and len(self.tags.all()) > 0:
            tags = [{'title': str(tag), 'href': '/search?id_tags={}'.format(str(tag)) } for tag in self.tags.all()]
            return tags
        return []

    def get_tags_as_list(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Used for ES indexing. At the moment stories do not have tags, but
        this might be added in the future.
        """
        return [str(tag) for tag in self.tags.all()]

    def get_search_representation(self):
        """
        Renders card for search result views.
        """
        return self.get_object_card_representation()

    def get_card_representation(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Decides what info to present on the "Discover collection in context" card.
        This card format also exist for stories, in a different color.
        """
        return MoleculeContextCardRegular(
            href=self.url,
            color='white',
            title=self.get_hero_info()['title'],
            type=self.get_category(),
            picture=self.get_primary_image()
        )

    def get_object_card_representation(self, classes=''):
        """
        Object specific card representation, for example for the "related" objects
        component. Search results are based on this template as well but not called from
        here but based on indexed data.
        """
        return MoleculeObjectCardRegular(
            href=self.url,
            title=self.get_hero_info()['title'],
            name=self.get_hero_info()['name'],
            picture=self.get_primary_image(),
            type=self.get_category(),
            classes=classes
        )

    def get_primary_image(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Image that is used if representing the object in a card or other component.
        TODO: return a default image if not found (objects without image can exist)
        """
        images = self.get_object_images()
        if images:
            return images[0]
        else:
            return None

    def get_raw_images(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Used when we need the raw images and not the atomized variant.
        """
        images = []
        for object in self.get_associated_objects():
           image_links = object.obj_img_link.all()
           for link in image_links:
               images.append(link.object_image)
        return images

    def get_primary_object(self):
        objects = self.get_associated_objects()
        try:
            return objects[0]
        except IndexError:
            return None

    def get_series_objects_as_cards(self):
        """
        Returns a list of clickable cards representing each object that is
        part of this series.
        """
        cards = []
        for o in self.get_associated_objects():
            try:
                page = MetaHubObjectPage.objects.get(object=o)
            except MetaHubObjectPage.DoesNotExist:
                pass
            else:
                cards.append(page.get_object_card_representation())
        return cards[:self.MAX_SHOWN_OBJECTS]

    def get_series_size(self):
        return len(self.get_associated_objects())

    def get_series_remaining_count(self):
        """
        Calculates the amount of elements that also belong to this series but
        are not shown yet in the grid.
        TODO: Localization support
        """
        total = self.get_series_size()
        if total <= self.MAX_SHOWN_OBJECTS:
            return None
        else:
            return 'Weitere Objekte dieser Serie ({})'.format(total - self.MAX_SHOWN_OBJECTS)

    def get_series_total_string(self):
        """
        Frontend formatted text for total count.
        """
        return 'Alle Objekte ({})'.format(self.get_series_size())

    def get_elasticsearch_series_id(self):
        """
        Used to generate prefiltered search results based on a series page
        and its objects. Since users can make series themselves we do this
        on page basis, not on series_id field since this is from BeeCollect.
        """
        try:
            return "object_series_{}".format(self.pk)
        except AttributeError:
            return None

    def get_all_objects_url(self):
        """
        Builds the url to prefiltered search page that will show all objects
        that belong to this series.
        Example: http://localhost:6767/search/?id_series=object_series_8252
        """
        return "{}?id_series={}".format(self.get_search_base_url(), self.get_elasticsearch_series_id())

    def get_object_images(self):
       """
       For each object that belongs to the series, retrieve its first image. These
       images are then shown on the series page and used in the header/lightbox.
       """
       image_list = []
       for object in self.get_associated_objects():
           images = object.obj_img_link.all()
           image_list += [AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image.object_image)) for image in
                    images]
       return image_list

    def get_object_artist(self):
        """
        Artist of the first object, we will treat this as the main artist.
        """
        object = self.get_primary_object()
        if object:
            if object.artist:
                return str(object.artist)
        return 'Unbekannt'

    def get_associated_objects(self):
        """
        Through the foreign relation, retrieve objects that belong to this series.
        An object can only belong to one series at a time.
        """
        return self.collection_objects.all()

    def build_metadata(self):
        """
        Create frontend-ready data for the metadata block.
        Series has no metadata block at the moment.
        """
        return []

    def get_favourite_info(self):
        """
        Specifies category and unique idenfifier for this page.
        """
        return {
            'category' : 'series',
            'id': self.pk
        }

    def save(self, *args, **kwargs):
        super().save(**kwargs)

        # If saving for the first time after creation,
        # add tags from the BeeCollect object to django-taggit
        if self.pk:
            if len(self.tags.all()) == 0:
                all_tags = []
                for object in self.get_associated_objects():
                    all_tags + object.get_bc_tags_as_list()
                self.tags.set(*all_tags)
            super().save(**kwargs)


class MetaHubStoryPage(AbstractMetaHubRichBasePage):
    """
    Page for the stories. These pages are not based on BeeCollect data but all
    made in the CMS.
    """

    # Used by Fork to retrieve story pages
    rest_api_id = models.CharField(max_length=100, default=None, null=True, blank=True)

    # The header is tightly connected to the introduction component, which inherits its contents
    hero_header = StreamField([
        ('header_image', OrganismHeroHeaderMultiImageRegularBlock()),
    ])

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('single_video', OrganismContentSingleVideoRegularBlock()),
        ('single_image', OrganismContentSingleImageRegularBlock()),
        ('single_audio', OrganismContentSingleAudioRegularBlock()),
        ('double_quote_richtext', OrganismContentDoubleQuoteRichTextRegularBlock()),
        ('double_pictures_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
    ])
    related_links = StreamField([('link_block', OrganismLinkListRegularBlock(max_num=1)),], blank=True )

    content_panels = AbstractMetaHubRichBasePage.content_panels + [
        ReadOnlyPanel('rest_api_id', heading="API identifier"),
        FieldPanel('collection_category'),
        StreamFieldPanel('hero_header'),
        StreamFieldPanel('content'),
        StreamFieldPanel('related_links'),
    ]

    def build_hero_header(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Created based on CMS panel, not automatically from BeeCollect.
        """
        header_child = self.hero_header[0]
        component = header_child.block.build_component(header_child.value)
        information = self.get_hero_info()
        return component._replace(information=information, context=self.has_context())

    def get_lightbox_items(self):
        """
        Get lightbox items and information. Since we need access to the properties
        of the MetaHubImage object we can't reuse get_object_images for this.
        """
        data = []
        try:
            header_child = self.hero_header[0]
        except IndexError:
            return []
        else:
            picture_structvalues = header_child.value['pictures']
            for sv in picture_structvalues:
                image = sv['source']
                image_data = {
                    'picture' : AtomPictureRegular(**Resolution(mobile='750', landscape='2048', crop=True).resolve(image)),
                    'information': {
                       'title' : self.title,
                       'name' : '',
                       'description': '',
                       'credits': image.attribution,
                    }
                }
                data.append(image_data)
        return data

    def get_hero_images(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Extracts the chosen images for the hero so that they can be reused in the
        intro component and lightbox component as well.
        """
        try:
            header_child = self.hero_header[0]
        except IndexError:
            return []
        else:
            picture_structvalues = header_child.value['pictures']
            return [AtomPictureRegular(**Resolution(mobile='1920', crop=True).resolve(sv['source'])) for sv in
                    picture_structvalues]

    def get_first_hero_image(self):
        try:
            header_child = self.hero_header[0]
        except IndexError:
            return []
        else:
            picture_structvalues = header_child.value['pictures']
            return picture_structvalues[0]

    def get_hero_info(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Determines information that is displayed in this page type's hero header.
        """
        return {
            'name' : self.get_category(),
            'title' : self.title
        }

    def get_search_representation(self):
        """
        Renders card for search result views.
        """
        return self.get_card_representation()


    def get_card_representation(self, classes=''):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Decides what info to present on the "Discover collection in context" card.
        """
        return MoleculeContextCardRegular(
            href=self.url,
            color='blurple',
            title=self.get_hero_info()['title'],
            type=self.get_category(),
            picture=self.get_primary_image(),
            classes=classes
        )

    def get_api_compatible_image(self):
        """
        Extracts MetaHubImage object source from the header so API can call
        rendition serializer.
        """
        try:
            header_child = self.hero_header[0]
        except IndexError:
            return None
        else:
            picture_structvalues = header_child.value['pictures']
            try:
                return picture_structvalues[0]['source']
            except IndexError:
                return None

    def get_primary_image(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Image that is used if representing the object in a card or other component.
        """
        images = self.get_hero_images()
        if len(images) > 0:
            return images[0]
        return None

    def get_elasticsearch_image(self):
        """
        Used by ElasticSearch, returns the path to the object's first image.
        TODO: Handle objects without image, this should return a placeholder ideally
        """
        image = self.get_first_hero_image()
        if image:
            try:
                image_data = ImageRenditionField('width-400').to_representation(image['source'])
                url = image_data['url']
            except AttributeError:
                return '/static/media/unsplash/cropped/search-result-2.jpg'
            else:
                return url
        return '/static/media/unsplash/cropped/search-result-2.jpg'

    def get_favourite_info(self):
        """
        Specifies category and unique identifier for this page.
        """
        return {
            'category' : 'story',
            'id': self.pk
        }

    def get_tags_as_list(self):
        """
        Overrides method from AbstractMetaHubRichBasePage
        Used for ES indexing. At the moment stories do not have tags, but
        this might be added in the future.
        """
        return []

    def save(self, *args, **kwargs):
        super().save(**kwargs)

        # Set REST API id
        if self.id:
            self.rest_api_id = "story_{}".format(self.id)
            super().save(**kwargs)


class MetaHubCategoryOverviewPage(metahubBasePage):
    """
    Functions as a categorization for the different kinds of pages in the collection.
    During sync with BeeCollect pages of the respective types are appended under
    this mother page. For this the first occurence is used.
    """
    overview_category = models.CharField(choices=[
        ('story', 'Story'),
        ('object', 'Objekt'),
        ('object_series', 'Objektseries'),
    ], max_length=100)

    content_panels = metahubBasePage.content_panels + [
        FieldPanel('overview_category')
    ]


class metahubImage(Image):
    alt_text = models.CharField(
        'Alt tekst',
        help_text="Optionele beschrijving van wat er in de afbeelding te zien is.",
        max_length=150,
        blank=True)

    attribution = models.CharField(
        'Credit',
        help_text="Artist credit or licensing information, leave blank if not applicable",
        max_length=4000,
        blank=True
    )

    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'attribution',
    )

    search_fields = list(Image.search_fields) + [
        index.SearchField('alt_text'),
        index.SearchField('attribution'),
    ]

    @property
    def relative_focal_point_x(self):
        if not self.focal_point_x:
            return .5
        # relative position
        relative_x = self.focal_point_x / self.width
        focal_correction = self.focal_point_width * relative_x
        if relative_x > .5:
            # correct towards right
            corrected_x = self.focal_point_x - ((self.focal_point_width / 2) - focal_correction)
        else:
            # correct towards left
            corrected_x = self.focal_point_x + ((self.focal_point_width / 2) - focal_correction)
        corrected_relative_x = corrected_x / self.width
        return corrected_relative_x

    @property
    def relative_focal_point_y(self):
        if not self.focal_point_y:
            return .5
        relative_y = self.focal_point_y / self.height
        focal_correction = self.focal_point_height * relative_y
        if relative_y > .5:
            # correct towards right
            corrected_y = self.focal_point_y - ((self.focal_point_height / 2) - focal_correction)
        else:
            # correct towards left
            corrected_y = self.focal_point_y + ((self.focal_point_height / 2) - focal_correction)
        corrected_relative_y = corrected_y / self.height
        return corrected_relative_y

    @property
    def relative_focal_point_percent(self):
        return '{}% {}%'.format(int(self.relative_focal_point_x * 100), int(self.relative_focal_point_y * 100))


@register_setting
class GlobalSettings(BaseSetting):
    """
    Global settings
    """
    default_share_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        verbose_name="Standaard share image",
        null=True,
        blank=True,
        help_text=_("Afbeelding voor op Facebook e.d. voor pagina\'s die zelf geen afbeelding hebben."),
        on_delete=models.SET_NULL,
        related_name='+'
    )

    default_site_description = models.CharField(
        blank=True,
        max_length=300,
        verbose_name="Meta description",
        help_text=_("Beschrijving van de site voor zoekmachine's e.d.")
    )

    footer_content_simple = StreamField(
        [('footer', StructureFooterBarSimpleBlock())]
    )

    def get_contextual_footer(self):
        if self.footer_content_simple:
            component = self.footer_content_simple[0].block.build_component(self.footer_content_simple[0].value)
            component = component._replace(context=True)
            return component

    def get_content_page_footer(self):
        if self.footer_content_simple:
            component = self.footer_content_simple[0].block.build_component(self.footer_content_simple[0].value)
            component = component._replace(content_page=True)
            return component

    panels = [
        ImageChooserPanel('default_share_image'),
        FieldPanel('default_site_description', classname="fullwidth", widget=Textarea(attrs={'rows': 2})),
        StreamFieldPanel('footer_content_simple'),
    ]

    class Meta:
        verbose_name = 'Algemene instellingen'
        verbose_name_plural = 'Algemene instellingen'


from random import randint

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.fields import StreamField

from metahub.collection.models.object_page import MetaHubObjectPage
from metahub.collection.models.object_series_page import MetaHubObjectSeriesPage
from metahub.core.models import MetaHubBasePage
from metahub.core.utils import MetaHubThemeColor, get_random_color


class MetaHubHomePage(RoutablePageMixin, MetaHubBasePage):
    """
    Homepage of the collection website. Features a header that supports livesearch, but
    directs user to search result when executing actual query. Other content includes a
    set of highlighted stories, objects and an overview of the collection categories.
    """

    def get_random_theme_color(self):
        return get_random_color()

    pass
    # search_header = StreamField([
    #     ('search_header', OrganismSearchHeaderRegularBlock())
    # ])
    #
    # theme_block = StreamField([
    #     ('theme_block', OrganismThemeHighlightsRegularBlock())
    # ])
    #
    # highlights_block = StreamField([
    #     ('highlights_block', OrganismObjectHighlightsRegularBlock())
    # ])
    #
    # collection_categories_block = StreamField([
    #     ('collection_categories_block', OrganismCollectionCategoriesRegularBlock())
    # ])
    #
    # content_panels = MetahubBasePage.content_panels + [
    #     StreamFieldPanel('search_header'),
    #     StreamFieldPanel('theme_block'),
    #     StreamFieldPanel('highlights_block'),
    #     StreamFieldPanel('collection_categories_block')
    # ]
    #
    # def get_random_header_picture(self):
    #     """
    #     Picks one of the chosen header images.
    #     """
    #     try:
    #         header_child = self.search_header[0]
    #     except IndexError:
    #         return None
    #     else:
    #         picture_structvalues = header_child.value['pictures']
    #         picture_index = randint(0, len(picture_structvalues) - 1)
    #         return picture_index
    #
    # def get_context(self, request, *args, **kwargs):
    #     context = super(MetaHubHomePage, self).get_context(request, *args, **kwargs)
    #     searchpage = MetaHubSearchPage.objects.all().specific()
    #     if len(searchpage):
    #         context['searchpage'] = searchpage[0]
    #     return context
    #
    # def get_collection_themes(self):
    #     """
    #     Based on the themes/stories chosen, retrieve the content needed to render frontend
    #     from these stories.
    #     """
    #     themes = self.theme_block[0]
    #     theme_cards = []
    #
    #     for element in themes.value['themes']:
    #         if element['page']:
    #             page = element['page'].specific
    #
    #             if element['intro_text'] and len(element['intro_text']) != 0:
    #                 text = element['intro_text']
    #             else:
    #                 text = page.highlight_intro
    #
    #             theme_cards.append({
    #                 'title': page.title,
    #                 'description': text,
    #                 'picture': page.get_primary_image(),
    #                 'background_images': page.get_hero_images()[1:],
    #                 'link': {
    #                             'href' : page.url,
    #                             'title': '',
    #                             'long_title': '',
    #                           }
    #             })
    #
    #     theme_categories = []
    #     for element in themes.value['theme_categories']:
    #         theme_categories.append(element)
    #
    #     data = OrganismThemeHighlightsRegular(
    #         title=themes.value['title'],
    #         subtitle=themes.value['subtitle'],
    #         theme_categories=theme_categories,
    #         themes=theme_cards
    #     )
    #     return data
    #
    # def get_object_highlights(self):
    #     """
    #     Objects of the collection that get the spotlight. A set of 5 objects is
    #     supported by the frontend. Since listblock does not seem to support
    #     min/max_num this is enforced here by slicing the list.
    #     """
    #     highlights = self.highlights_block[0]
    #     highlight_cards = []
    #
    #     for element in highlights.value['highlights']:
    #         page = element['page'].specific
    #
    #         # Check if the highlight has text
    #         text = element['intro_text'] if not None else page.highlight_intro
    #
    #         # Get object
    #         object = None
    #         if isinstance(page, MetaHubObjectPage):
    #             object = page.object
    #         elif isinstance(page, MetaHubObjectSeriesPage):
    #             object = page.get_primary_object()
    #
    #         # Build card (it does not use a molecule)
    #         highlight_cards.append({
    #             'href' : page.url,
    #             'description': text,
    #             'title' : page.title,
    #             'picture' : page.get_primary_image(),
    #             'detail' : page.get_object_artist(), # Page type is enforced by chooser block
    #             'subdetail': page.get_type_dating(),
    #             'location' : object.current_location,
    #         })
    #
    #     # Build component as a whole
    #     return OrganismObjectHighlightsRegular(
    #         title=highlights.value['title'],
    #         introduction=highlights.value['introduction'],
    #         cards=highlight_cards[:5],
    #         all_highlights_url="{}?id_is_highlight=true".format(self.get_search_base_url())
    #     )

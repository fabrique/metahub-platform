from django.shortcuts import redirect
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.core.utils import MetaHubThemeColor, get_random_color

from metahub.news.utils import get_all_news_and_events
from metahub.starling_metahub.organisms.blocks import OrganismHomeIntroRegularBlock, \
    OrganismArticleCuratedObjectsRegularBlock, OrganismHomeFeaturedStoryBlock, \
    OrganismArticleCuratedNewsRegularBlock, \
    OrganismArticleRelatedNewsRegularBlock


class MetaHubHomePage(RoutablePageMixin, MetaHubBasePage):
    """
    Homepage of the collection website. Features a header that supports livesearch, but
    directs user to search result when executing actual query. Other content includes a
    set of highlighted stories, objects and an overview of the collection categories.
    """

    max_count_per_parent = 1
    parent_page_types = ['wagtailcore.Page', 'home.MetaHubHomePage']

    home_intro = StreamField(StreamBlock([
        ('home_intro', OrganismHomeIntroRegularBlock()),
    ], max_num=1))

    object_highlights = StreamField(StreamBlock([
        ('object_highlights', OrganismArticleCuratedObjectsRegularBlock(defaults={'classes' : 'relevant-objects--home'}, required=False)),
    ], max_num=1, required=False), blank=True)

    story_highlight = StreamField(StreamBlock([
        ('story_highlight', OrganismHomeFeaturedStoryBlock()),
    ], max_num=1))

    news_highlights = StreamField(StreamBlock([
        ('related_curated', OrganismArticleCuratedNewsRegularBlock()),
        ('related_automatic', OrganismArticleRelatedNewsRegularBlock()),
    ], max_num=1))

    content_panels = MetaHubBasePage.content_panels + [
        StreamFieldPanel('home_intro'),
        StreamFieldPanel('object_highlights'),
        StreamFieldPanel('story_highlight'),
        StreamFieldPanel('news_highlights')
    ]

    def get_random_theme_color(self):
        return get_random_color()

    def get_page_related_items(self):
        return get_all_news_and_events()[:3]


class MetaHubMuseumSubHomePage(MetaHubBasePage):
    """ This class represents a museum that participates in the MetaHub.
    Objects and stories are placed under a specific museum. """

    parent_page_types = ['home.MetaHubHomePage']

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_site().root_url)

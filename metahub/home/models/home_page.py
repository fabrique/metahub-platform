
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.core.utils import MetaHubThemeColor, get_random_color
from metahub.starling_metahub.organisms.blocks import OrganismHomeIntroRegularBlock, \
    OrganismArticleRelatedItemsRegularBlock, OrganismArticleCuratedObjectsRegularBlock


class MetaHubHomePage(RoutablePageMixin, MetaHubBasePage):
    """
    Homepage of the collection website. Features a header that supports livesearch, but
    directs user to search result when executing actual query. Other content includes a
    set of highlighted stories, objects and an overview of the collection categories.
    """

    max_count_per_parent = 1
    parent_page_types = ['wagtailcore.Page']

    home_intro = StreamField(StreamBlock([
        ('home_intro', OrganismHomeIntroRegularBlock()),
    ], max_num=1))

    object_highlights = StreamField(StreamBlock([
        ('object_highlights', OrganismArticleCuratedObjectsRegularBlock(defaults={'classes' : 'relevant-objects--home'})),
    ], max_num=1))

    # story_highlight = StreamField(StreamBlock([
    #     ('object_highlights', OrganismArticleRelatedItemsRegularBlock()),
    # ], max_num=1))

    content_panels = MetaHubBasePage.content_panels + [
        StreamFieldPanel('home_intro'),
        StreamFieldPanel('object_highlights'),
    ]



    def get_random_theme_color(self):
        return get_random_color()


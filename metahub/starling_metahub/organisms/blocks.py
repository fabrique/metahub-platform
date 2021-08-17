from django.utils.translation import ugettext_lazy as _

from starling.blocks.atoms.figure import AtomFigureRegularBlock
from starling.blocks.atoms.link import AtomLinkRegularBlock
from starling.blocks.atoms.picture import AtomPictureRegularBlock
from starling.interfaces.generic import Resolution
from starling.mixins import AdapterStructBlock, OptionalBlock
from wagtail.core import blocks
from wagtail.core.blocks import ListBlock

from .interfaces import *
from ..atoms.blocks import AtomVideoEmbedRegularBlock
from ..helpers import HelperRelatedPagesBlock, HelperRelatedPageBlock, HelperRelatedObjectsBlock, \
    HelperRelatedStoriesBlock, HelperRelatedStoryBlock
from ..utils import count_words_html
from ...core.utils import format_date


class OrganismHeroImageHeaderRegularBlock(AdapterStructBlock):
    """
    Content Page Header Component
    Simple header with an image
    """
    picture = AtomPictureRegularBlock(resolution=Resolution(mobile="1920x1080"))

    class Meta:
        label = _("Header image")
        icon = 'image'
        component = 'organisms.hero-image.regular'
        interface_class = OrganismHeroImageHeaderRegular


class OrganismHeroTextHeaderRegularBlock(AdapterStructBlock):
    """
    Content Page Header Component
    Header with text
    """
    title = blocks.CharBlock(max_length=200)
    text = blocks.TextBlock(max_length=2000)

    class Meta:
        icon = 'title'
        label = _("Header text")
        component = 'organisms.hero-text.regular'
        interface_class = OrganismHeroTextHeaderRegular


class OrganismHeroTextHeaderExtraInfoBlock(OrganismHeroTextHeaderRegularBlock):
    def build_extra(self, value, build_args, parent_context=None):
        page = (parent_context or {}).get('page')

        if not page:
            return

        build_args.update({
            'date': format_date(page.date),
            'author': ', '.join(page.get_page_authors()),
        })


class OrganismContentSingleRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a single richtext component
    """
    text = blocks.RichTextBlock()

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        label = _("Text")
        icon = 'pilcrow'
        component = 'organisms.article-content.regular'
        interface_class = OrganismContentSingleRichTextRegular


class OrganismContentSingleImageRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a single image with a caption
    """
    figure = AtomFigureRegularBlock([
        ('picture', AtomPictureRegularBlock(resolution=Resolution(mobile='1920', crop=True))),
    ])

    class Meta:
        label = _("Photo")
        icon = 'image'
        component = 'organisms.article-photo.regular'
        interface_class = OrganismContentSingleImageRegular


class OrganismContentSingleVideoRegularBlock(AdapterStructBlock):
    """
    Content Component
    Supports Vimeo and YouTube uploads. Includes an optional link to
    a video transcript for accessiblity purposes.
    """
    video = AtomVideoEmbedRegularBlock(required=True)
    caption = blocks.CharBlock(required=False)

    class Meta:
        label = _("Video")
        icon = 'media'
        component = 'organisms.article-video.temporarybackend'
        interface_class = OrganismContentSingleVideoRegular


class OrganismContentDoubleImageRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a richtext on the left and a picture with caption on the right.
    Optionally includes a link as well.
    """
    figure = AtomFigureRegularBlock()
    text = blocks.RichTextBlock(required=True)

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        label = _("Text and image")
        icon = 'image'
        defaults = {}
        component = 'organisms.content-and-image.regular'
        interface_class = OrganismContentDoubleImageRichTextRegular


class OrganismContentDoubleLinkRichTextRegularBlock(AdapterStructBlock):
    """
    Content Component
    Renders a richtext on the left and a picture with caption on the right.
    Optionally includes a link as well.
    """
    text = blocks.RichTextBlock(required=True)
    link = OptionalBlock(AtomLinkRegularBlock())

    def get_word_count(self, value):
        return count_words_html(value['text'])

    class Meta:
        label = _("Text and link")
        icon = 'link'
        component = 'organisms.content-and-link.regular'
        interface_class = OrganismContentDoubleLinkRichTextRegular


class OrganismContentHeroImageTitleBlock(AdapterStructBlock):
    """
    Content Component
    Image with title and link, call to action/highlight
    """
    title = blocks.CharBlock(max_length=200)
    link = AtomLinkRegularBlock()
    picture = AtomPictureRegularBlock()

    class Meta:
        label = _("Hero highlight")
        icon = 'pick'
        component = 'organisms.hero-image-title.regular'
        interface_class = OrganismContentHeroImageTitle


class OrganismContentPhotoMosaicBlock(AdapterStructBlock):
    """
    Content Component
    A list of pictures placed playfully
    """
    figures = ListBlock(AtomFigureRegularBlock())

    class Meta:
        label = _("Photo mosaic")
        icon = 'image'
        component = 'organisms.images.regular'
        interface_class = OrganismContentPhotoMosaic


class OrganismArticleCookieBlockRegular(AdapterStructBlock):
    title = blocks.CharBlock()
    text = blocks.TextBlock()

    class Meta:
        label = _("Cookie settings")
        icon = 'cogs'
        component = 'organisms.article-cookies.regular'
        interface_class = OrganismArticleCookieRegular


class OrganismArticleCuratedItemsRegularBlock(AdapterStructBlock):
    """
    Basic/Content Page component
    Allows linking to another page through clickable cards.
    """

    title = blocks.CharBlock(max_length=100)
    items = HelperRelatedPagesBlock()

    class Meta:
        label = _("Related items (curated)")
        icon = 'arrows-up-down'
        defaults = {}
        component = 'organisms.relevant-cards.story'
        interface_class = OrganismArticleRelatedItemsRegular


class OrganismArticleCuratedObjectsRegularBlock(OrganismArticleCuratedItemsRegularBlock):
    items = HelperRelatedPagesBlock()

    class Meta:
        label= "Related/highlighted items"
        component = 'organisms.relevant-cards.object'


class OrganismArticleCuratedStoriesRegularBlock(OrganismArticleCuratedItemsRegularBlock):
    items = HelperRelatedPagesBlock()

    class Meta:
        label = "Related/highlighted items"
        component = 'organisms.relevant-cards.story'


class OrganismArticleCuratedNewsRegularBlock(OrganismArticleCuratedItemsRegularBlock):
    items = HelperRelatedPagesBlock()
    link = AtomLinkRegularBlock()

    class Meta:
        label = "Related/highlighted news and events"
        component = 'organisms.relevant-cards.news'
        interface_class = OrganismArticleRelatedItemsWithLinkRegular


class OrganismArticleRelatedItemsRegularBlock(AdapterStructBlock):
    """
    Basic/Content Page component
    Creates a set of related items based on type
    """
    title = blocks.CharBlock(max_length=100)

    def build_extra(self, value, build_args, parent_context=None):
        page = (parent_context or {}).get('page')

        if not page:
            return

        build_args.update({
            'cards' : [page.get_card_representation() for page in page.get_page_related_items()]
        })

    class Meta:
        label = _("Related items (automatic)")
        icon = 'arrows-up-down'
        defaults = {}
        component = 'organisms.relevant-cards.story'
        interface_class = OrganismArticleRelatedItemsRegular


class OrganismArticleRelatedObjectsRegularBlock(OrganismArticleRelatedItemsRegularBlock):
    class Meta:
        component = 'organisms.relevant-cards.object'
        interface_class = OrganismArticleRelatedItemsRegular


class OrganismArticleRelatedStoriesRegularBlock(OrganismArticleRelatedItemsRegularBlock):
    class Meta:
        component = 'organisms.relevant-cards.story'
        interface_class = OrganismArticleRelatedItemsRegular


class OrganismArticleRelatedNewsRegularBlock(OrganismArticleRelatedItemsRegularBlock):
    link = AtomLinkRegularBlock()

    class Meta:
        component = 'organisms.relevant-cards.news'
        interface_class = OrganismArticleRelatedItemsWithLinkRegular


class OrganismActualitiesLandingHeaderRegularBlock(AdapterStructBlock):
    """
    Actualities Landing Page component
    A simple header with text and a featured item (either news or event)
    """
    featured_item = HelperRelatedPageBlock()
    excerpt = blocks.TextBlock()
    link_label = blocks.CharBlock(default=_('Read more'), max_length=200)

    def build_extra(self, value, build_args, parent_context=None):
        page = (parent_context or {}).get('page')

        if not page:
            return

        build_args.update({
            'title': page.title
        })

    class Meta:
        label = _("Header with featured item")
        icon = 'title'
        component = 'organisms.news-list-intro.regular'
        interface_class = OrganismFeaturedCardRegular


class OrganismHomeIntroRegularBlock(AdapterStructBlock):
    """
    Simple introduction block for the home with title and text
    """
    title = blocks.CharBlock(max_length=200)
    text = blocks.RichTextBlock(features=['link'])

    class Meta:
        label = _("Home intro")
        icon = 'form'
        component = 'organisms.home-content.regular'
        interface_class = OrganismHomeIntroRegular


class OrganismHomeFeaturedStoryBlock(AdapterStructBlock):
    """
    A block that highlights a single story, looks similar to the featured
    news/event on the actualities page
    """
    title = blocks.CharBlock(max_length=100)
    featured_item = HelperRelatedStoryBlock()
    excerpt = blocks.TextBlock()
    link_label = blocks.CharBlock(default=_('Read more'), max_length=200)
    all_stories_link_label = blocks.CharBlock(default=_('See all stories'), max_length=200)

    # def build_extra(self, value, build_args, parent_context=None):
    #     from metahub.search.models import MetaHubSearchPage
    #     try:
    #         search_page = MetaHubSearchPage.objects.live().first()
    #     except MetaHubSearchPage.DoesNotExist:
    #         return
    #     else:
    #         build_args.update({
    #             'link': AtomLinkRegular(href=f"{search_page.url}?id_type=story",
    #                                     title=value['all_stories_link_label'])
    #         })

    class Meta:
        label = _("Highlighted story")
        icon = 'pick'
        component = 'organisms.highlighted-card.regular'
        interface_class = OrganismFeaturedCardLinkToAllRegular
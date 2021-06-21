from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismHeroHeaderSingleImageContentPageRegularBlock, \
    OrganismContentSingleRichTextRegularBlock, OrganismContentSingleImageRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismArticleCookieBlockRegular


class MetaHubContentPage(MetaHubBasePage):

    parent_page_types = ['home.MetahubHomePage']

    hero_header = StreamField([
        ('header_image', OrganismHeroHeaderSingleImageContentPageRegularBlock()),
    ])

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('single_image', OrganismContentSingleImageRegularBlock()),
        ('double_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        # ('cookies', OrganismArticleCookieBlockRegular())
    ])

    content_panels = MetaHubBasePage.content_panels + [
        StreamFieldPanel('hero_header'),
        StreamFieldPanel('content')
    ]
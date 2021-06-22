from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismContentSingleRichTextRegularBlock, OrganismContentSingleImageRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismArticleCookieBlockRegular, \
    OrganismHeroTextHeaderRegularBlock, OrganismContentSingleVideoRegularBlock, OrganismContentHeroImageTitleBlock, \
    OrganismContentPhotoMosaicBlock


class MetaHubContentPage(MetaHubBasePage):

    parent_page_types = ['home.MetahubHomePage']

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ], blank=True)
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderRegularBlock()),
    ])

    # CMS panels
    content = StreamField([
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        # ('single_image', OrganismContentSingleImageRegularBlock()),
        ('double_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('video', OrganismContentSingleVideoRegularBlock()),
        ('highlight', OrganismContentHeroImageTitleBlock()),
        ('image_mosaic', OrganismContentPhotoMosaicBlock())
        # ('cookies', OrganismArticleCookieBlockRegular())
    ])

    content_panels = MetaHubBasePage.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading="Header"),
        StreamFieldPanel('content')
    ]
from starling.interfaces.atoms import AtomPictureRegular
from starling.interfaces.generic import Resolution
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField

from metahub.content.blocks import content_blocks
from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismHeroImageHeaderRegularBlock, \
    OrganismContentSingleRichTextRegularBlock, OrganismContentSingleImageRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismArticleCookieBlockRegular, \
    OrganismHeroTextHeaderRegularBlock, OrganismContentSingleVideoRegularBlock, OrganismContentHeroImageTitleBlock, \
    OrganismContentPhotoMosaicBlock, OrganismArticleCuratedItemsRegularBlock


class MetaHubContentPage(MetaHubBasePage):

    parent_page_types = ['home.MetahubHomePage']

    hero_header = StreamField([
        ('header_image', OrganismHeroImageHeaderRegularBlock()),
    ], blank=True)
    text_header = StreamField([
        ('header_text', OrganismHeroTextHeaderRegularBlock()),
    ])

    content = StreamField(content_blocks(), blank=True)

    related_items = StreamField([
        ('related_curated', OrganismArticleCuratedItemsRegularBlock())
    ], blank=True)

    content_panels = MetaHubBasePage.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('hero_header'),
            StreamFieldPanel('text_header'),
        ], heading="Header"),
        StreamFieldPanel('content'),
        StreamFieldPanel('related_items')
    ]

    def get_page_label(self):
        return 'Sample label'

    def get_page_header_image(self):
        """ Used in the card representation.
        TODO: Optional override through promo img? """
        try:
            header_child = self.hero_header[0]
        except IndexError:
            return
        else:
            picture_structvalue = header_child.value['picture']
            return AtomPictureRegular(**Resolution(mobile='1920', crop=True).resolve(picture_structvalue['source']))
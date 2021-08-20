from metahub.starling_metahub.organisms.blocks import OrganismContentSingleRichTextRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismContentSingleVideoRegularBlock, \
    OrganismContentHeroImageTitleBlock, OrganismContentPhotoMosaicBlock, OrganismContentDoubleLinkRichTextRegularBlock, \
    OrganismArticleCookieBlockRegular, OrganismSponsorsRegularBlock


def content_blocks():
    return [
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('two_column_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('richtext_with_link', OrganismContentDoubleLinkRichTextRegularBlock()),
        ('video', OrganismContentSingleVideoRegularBlock()),
        ('highlight', OrganismContentHeroImageTitleBlock()),
        ('image_mosaic', OrganismContentPhotoMosaicBlock()),
        ('sponsor_logos', OrganismSponsorsRegularBlock()),
        ('cookie_settings', OrganismArticleCookieBlockRegular()),
    ]

def cookieless_content_blocks():
    """ No cookies for this block set awwwwwwww
    See CNV for a more elegant variant of restricting blocks per page type """
    return [
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('two_column_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('richtext_with_link', OrganismContentDoubleLinkRichTextRegularBlock()),
        ('video', OrganismContentSingleVideoRegularBlock()),
        ('highlight', OrganismContentHeroImageTitleBlock()),
        ('image_mosaic', OrganismContentPhotoMosaicBlock()),
    ]
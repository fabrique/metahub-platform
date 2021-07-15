from metahub.starling_metahub.organisms.blocks import OrganismContentSingleRichTextRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismContentSingleVideoRegularBlock, \
    OrganismContentHeroImageTitleBlock, OrganismContentPhotoMosaicBlock, OrganismContentDoubleLinkRichTextRegularBlock


def content_blocks():
    return [
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('two_column_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('richtext_with_link', OrganismContentDoubleLinkRichTextRegularBlock()),
        ('video', OrganismContentSingleVideoRegularBlock()),
        ('highlight', OrganismContentHeroImageTitleBlock()),
        ('image_mosaic', OrganismContentPhotoMosaicBlock()),
    ]
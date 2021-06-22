from metahub.starling_metahub.organisms.blocks import OrganismContentSingleRichTextRegularBlock, \
    OrganismContentDoubleImageRichTextRegularBlock, OrganismContentSingleVideoRegularBlock, \
    OrganismContentHeroImageTitleBlock, OrganismContentPhotoMosaicBlock

def content_blocks():
    return [
        ('single_richtext', OrganismContentSingleRichTextRegularBlock()),
        ('double_picture_richtext', OrganismContentDoubleImageRichTextRegularBlock()),
        ('video', OrganismContentSingleVideoRegularBlock()),
        ('highlight', OrganismContentHeroImageTitleBlock()),
        ('image_mosaic', OrganismContentPhotoMosaicBlock()),
    ]
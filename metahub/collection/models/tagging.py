from django.db import models

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class BaseTag(models.Model):
    """
    Tag attached to the OBJECT MODEL. The tags come out of BeeCollect in the form
    of a comma-separated string. We store these original tags with this model.
    Each object can have multiple tags and each tag can belong to multiple objects.
    """
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class CollectionObjectTag(TaggedItemBase):
    """
    Tag attached to the OBJECT PAGE, these tags are inferred from BeeCollect
    upon import but can also be changed and added upon in the CMS.
    """
    content_object = ParentalKey(
        'core.MetaHubObjectPage',
        related_name='tagged_objects',
        on_delete=models.CASCADE,
    )


class CollectionObjectSeriesTag(TaggedItemBase):
    """
    Tag attached to the OBJECT SERIES PAGE. These are an aggregate of the objects
    that are a part of this series, and created at sync time. They can be changed
    and expanded upon in the CMS.
    """
    content_object = ParentalKey(
        'core.MetaHubObjectSeriesPage',
        related_name='tagged_object_series',
        on_delete=models.CASCADE,
    )

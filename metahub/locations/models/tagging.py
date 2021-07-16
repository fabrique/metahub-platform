from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

class LocationTag(TaggedItemBase):
    content_object = ParentalKey(
        'locations.MetaHubLocationPage',
        related_name='tagged_objects',
        on_delete=models.CASCADE,
    )
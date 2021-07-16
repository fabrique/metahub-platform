from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class StoryTag(TaggedItemBase):
    content_object = ParentalKey(
        'stories.MetaHubStoryPage',
        related_name='tagged_objects',
        on_delete=models.CASCADE,
    )
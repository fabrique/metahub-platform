from django.db import models
from wagtail.admin.edit_handlers import FieldPanel

from metahub.core.models import MetahubBasePage


class MetaHubCategoryOverviewPage(MetahubBasePage):
    """
    Functions as a categorization for the different kinds of pages in the collection.
    During sync with BeeCollect pages of the respective types are appended under
    this mother page. For this the first occurrence is used.
    """
    overview_category = models.CharField(choices=[
        ('story', 'Story'),
        ('object', 'Objekt'),
        ('object_series', 'Objektseries'),
    ], max_length=100)

    content_panels = MetahubBasePage.content_panels + [
        FieldPanel('overview_category')
    ]

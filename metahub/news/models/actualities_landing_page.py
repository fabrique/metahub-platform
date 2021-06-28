from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.starling_metahub.organisms.blocks import OrganismActualitiesLandingHeaderRegularBlock


class MetaHubActualitiesLandingPage(MetaHubBasePage):
    """
    This page is the landing for an overview of both events
    and news.
    """
    parent_page_types = ['home.MetaHubHomePage']

    header = StreamField([
        ('header', OrganismActualitiesLandingHeaderRegularBlock()),
    ])

    content_panels = MetaHubBasePage.content_panels + [
        FieldPanel('theme_color'),
        StreamFieldPanel('header'),
    ]



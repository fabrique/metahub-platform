from django.core.paginator import PageNotAnInteger
from pure_pagination import Paginator
from django.utils.translation import ugettext_lazy as _

from starling.interfaces.atoms import AtomLinkRegular
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from metahub.core.models import MetaHubBasePage
from metahub.news.utils import get_all_news_and_events
from metahub.starling_metahub.atoms.interfaces import AtomPaginationButtonRegular
from metahub.starling_metahub.molecules.interfaces import MoleculePaginationRegular
from metahub.starling_metahub.organisms.blocks import OrganismActualitiesLandingHeaderRegularBlock
from metahub.starling_metahub.organisms.interfaces import OrganismCardGridRegular
from metahub.starling_metahub.utils import create_paginator_component


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

    def get_all_news_and_events(self):
        return get_all_news_and_events()

    def get_actualities_landing_grid_component(self, paginated_list):
        return OrganismCardGridRegular(
            title='Latest',
            cards=[p.get_card_representation() for p in paginated_list]
        )

    def create_paginator_component(self, paginator, paginator_page):
        return create_paginator_component(paginator, paginator_page)

    def get_context(self, request, *args, **kwargs):
        context = super(MetaHubActualitiesLandingPage, self).get_context(request, *args, **kwargs)

        # Obtain and validate page number
        MAX_ITEMS_PER_PAGE = 12
        page_number = request.GET.get('page', 1)
        paginator = Paginator(self.get_all_news_and_events(), request=request, per_page=MAX_ITEMS_PER_PAGE)

        try:
            page = paginator.validate_number(page_number)
        except PageNotAnInteger:
            page = 1

        paginator_page = paginator.page(page)

        context.update({
            'actualities_landing_grid_component': self.get_actualities_landing_grid_component(paginator_page.object_list),
            'paginator': self.create_paginator_component(paginator, paginator_page),
        })

        return context



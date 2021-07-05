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

    def get_context(self, request, *args, **kwargs):
        context = super(MetaHubActualitiesLandingPage, self).get_context(request, *args, **kwargs)

        # Obtain and validate page number
        MAX_ITEMS_PER_PAGE = 6
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

    def create_paginator_component(self, paginator, paginator_page):
        # Don't show paginator for single page
        if paginator.num_pages == 1:
            return

        # Create pagination object
        buttons = []
        for page in paginator_page.pages():
            if page:
                buttons.append(AtomPaginationButtonRegular(
                    title=page,
                    href=f'?page={page}',
                    current=int(page) is int(paginator_page.number)
                ))
            else:
                buttons.append('...')

        # Separate buttons for previous and next
        button_previous = AtomLinkRegular(
            title=_('Vorige'),
            href=f'?page={paginator_page.number - 1}'
        ) if paginator_page.number > 1 else None

        button_next = AtomLinkRegular(
            title=_('Volgende'),
            href=f'?page={paginator_page.number + 1}'
        ) if paginator_page.number < paginator.num_pages else None

        return MoleculePaginationRegular(
            button_previous=button_previous,
            button_next=button_next,
            buttons=buttons
        )



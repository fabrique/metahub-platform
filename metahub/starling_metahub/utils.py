from django.utils.html import strip_tags
import re
from django.utils.translation import ugettext_lazy as _

from starling.interfaces.atoms import AtomLinkRegular

from metahub.starling_metahub.atoms.interfaces import AtomPaginationButtonRegular
from metahub.starling_metahub.molecules.interfaces import MoleculePaginationRegular


def count_words_html(html):
    return count_words(strip_tags(html))


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def create_paginator_component(paginator, paginator_page):
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
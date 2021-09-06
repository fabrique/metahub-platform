from django.core.validators import validate_slug
from django.utils.html import strip_tags
import re
from django.utils.translation import ugettext_lazy as _
from starling.forms import starlize_form

from starling.interfaces.atoms import AtomLinkRegular, AtomButtonButton
from starling.interfaces.molecules import MoleculeFormRegular
from starling.mixins import AdapterStructBlock
from wagtail.core import blocks

from starling.renderables.models import RAtomFormFieldsetRegular, RAtomFormRowRegular
from metahub.starling_metahub.atoms.interfaces import AtomPaginationButtonRegular
from metahub.starling_metahub.molecules.interfaces import MoleculePaginationRegular
from metahub.streamforms.blocks import FabriqueFormBlock, FilteredFormChooserBlock
from metahub.streamforms.utils import get_field_structure


def count_words_html(html):
    return count_words(strip_tags(html))


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def create_paginator_component(paginator, paginator_page, querystring_extra=''):
    # Don't show paginator for single page
    if paginator.num_pages == 1:
        return

    # Create pagination object
    buttons = []
    for page in paginator_page.pages():
        if page:
            buttons.append(AtomPaginationButtonRegular(
                title=page,
                href=f'?page={page}{querystring_extra}',
                current=int(page) is int(paginator_page.number)
            ))
        else:
            buttons.append('...')

    # Separate buttons for previous and next
    button_previous = AtomLinkRegular(
        # title=_('Vorige'),
        href=f'?page={paginator_page.number - 1}{querystring_extra}'
    ) if paginator_page.number > 1 else None

    button_next = AtomLinkRegular(
        # title=_('Volgende'),
        href=f'?page={paginator_page.number + 1}{querystring_extra}'
    ) if paginator_page.number < paginator.num_pages else None

    return MoleculePaginationRegular(
        button_previous=button_previous,
        button_next=button_next,
        buttons=buttons
    )

def get_single_field_structure(streamform, form):
    structure = get_field_structure(streamform)
    return [
        form[structure['field']],
        *(form[field_name] for field_name in structure['meta'])
    ]


def get_multi_field_structure(streamform, form):
    """ Convert a StreamForm to a Starling renderable structure """
    def build_row(row):
        if isinstance(row, dict) and 'fields' in row:
            return RAtomFormRowRegular(
                content=[form[field_name] for field_name in row['fields']]
            )
        return form[row]
    structure = get_field_structure(streamform)
    return [
        *(RAtomFormFieldsetRegular(
            title=field_set['title'],
            content=[build_row(row) for row in field_set['rows']],
         )
         for field_set in structure['field_sets']),
        *(form[field_name] for field_name in structure['meta'])
    ]


def streamform_to_renderable(streamform, form):
    structure = get_field_structure(streamform)
    if structure['type'] == 'single_field':
        return get_single_field_structure(streamform, form)
    elif structure['type'] == 'multi_field':
        return get_multi_field_structure(streamform, form)


class StreamFormBlockMixin(AdapterStructBlock, FabriqueFormBlock):
    """
    Helper for blocks that render streamforms
    """
    form = FilteredFormChooserBlock

    def build_extra(self, value, build_args, parent_context=None):
        context = self.get_context(value, parent_context)
        del build_args['form']
        del build_args['form_action']
        del build_args['form_reference']
        stream_form = value.get("form")
        if stream_form:
            stream_form_template = getattr(
                stream_form,
                'template',
                'qm_starling/streamform_body.html',
            )
            # ignoring template for now
            form_renderable = streamform_to_renderable(
                stream_form,
                starlize_form(context['form']))
            build_args.update({
                'form': MoleculeFormRegular(
                    action=value['form_action'],
                    button=AtomButtonButton(
                        title=stream_form.submit_button_text,
                        type='submit',
                        variant='primary'
                    ),
                    content=form_renderable,
                    csrf=context.get('csrf_token'),
                ),
            })

    def render(self, value, context=None):
        # We skip the stream form rendering, since it blocks Starling's
        return self.render_basic(value, context)


# def force_csrf_token_on_request(request):
#     if 'CSRF_COOKIE' not in request.META:
#         rotate_token(request)


class OrganismBlockMixin(AdapterStructBlock):

    def __init__(self, blocks=[], local_blocks=(), **kwargs):
        internal_blocks = []

        for block in blocks:
            internal_block = getattr(self, block.upper(), None)

            if internal_block:
                internal_blocks.append(tuple(internal_block))

        if internal_blocks and len(internal_blocks):
            local_blocks += tuple(internal_blocks)

        super().__init__(local_blocks, **kwargs)


    class Meta:
        abstract = True

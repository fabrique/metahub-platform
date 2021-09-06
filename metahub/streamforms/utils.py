"""
Utility functions for wagtailstream_forms
"""
from django.core.exceptions import ImproperlyConfigured
from wagtail.core import blocks
from wagtailstreamforms.fields import get_fields, BaseField
from wagtailstreamforms.streamfield import FormFieldStreamBlock
from wagtailstreamforms.utils.general import get_slug_from_string


class NonRecursiveFormFieldStreamBlock(FormFieldStreamBlock):
    """ FormFieldStreamBlock that doesn't recursively add itself as option """

    def __init__(self, local_blocks=None, **kwargs):
        self._constructor_kwargs = kwargs

        super(blocks.BaseStreamBlock, self).__init__(**kwargs)  # added kwarg passing

        self._child_blocks = self.base_blocks.copy()

        for name, field_class in get_fields().items():
            if self.meta.include and name not in self.meta.include:
                continue

            if name in self.meta.exclude:
                continue

            # ensure the field is a subclass of BaseField.
            if not issubclass(field_class, BaseField):
                raise ImproperlyConfigured(
                    "'%s' must be a subclass of '%s'" % (field_class, BaseField)
                )

            # assign the block
            block = field_class().get_form_block()
            block.set_name(name)
            self._child_blocks[name] = block

        self._dependencies = self._child_blocks.values()

    class Meta:
        exclude = ()
        include = ()


def get_single_field_structure(fields):
    registered_fields = get_fields()
    field = fields[0]
    registered_cls = registered_fields[field.get('type')]()
    field_name = registered_cls.get_formfield_name(field.get('value'))
    return {
        'type': 'single_field',
        'field': field_name,
        'meta': ['form_id', 'form_reference']
    }


def get_multi_field_structure(fields):
    from metahub.streamforms.wagtailstreamforms_fields import FieldsetField
    registered_fields = get_fields()
    structure = {
        'type': 'multi_field',
        'field_sets': [],
        'meta': ['form_id', 'form_reference'],
    }
    fieldsets = structure['field_sets']
    for fieldset in fields:
        fieldset_structure = {
            'title': FieldsetField.get_formfield_label(fieldset['value']),
            'rows': [],
        }

        for form_row in fieldset['value']['form_fields']: #loop over form rows from CMS
            if 'form_fields' in form_row['value']:
                fields = []
                for field in form_row['value']['form_fields']:
                    registered_cls = registered_fields[field.get('type')]()
                    field_name = registered_cls.get_formfield_name(field.get('value'))
                    fields.append(field_name)
                fieldset_structure['rows'] += fields   #MKR slight refactor, since we dont need multi column forms

        fieldsets.append(fieldset_structure)

    return structure


def get_field_structure(form):
    """ Get a structure that shows how the fieldsets and form rows relate the fields """
    form_type = form.fields.stream_data[0]

    if form_type['type'] == 'single_field':
        return get_single_field_structure(form_type['value']['form_fields'])
    if form_type['type'] == 'multi_field':
        return get_multi_field_structure(form_type['value']['form_fields'])


def get_fields_flat(form):
    """ Return a non nested list of form fields """
    if not len(form.fields.stream_data):
        return
    # FIXME: is there a cleaner way to get identical data from stream_data whether lazy or not?
    is_lazy = form.fields.is_lazy
    form_type = form.fields.stream_data[0]
    form_type = form_type if is_lazy else {'type': form_type[0], 'value': form_type[1]}
    if form_type['type'] == 'single_field':
        for field in form_type['value']['form_fields']:
            field = field if is_lazy else {'type': field.block.name, 'value': field.value}
            yield field
        return

    for fieldset in form_type['value']['form_fields']:
        fieldset = fieldset if is_lazy else {'type': fieldset.block.name, 'value': fieldset.value}
        yield fieldset
        for form_row in fieldset['value']['form_fields']:
            form_row = form_row if is_lazy else {'type': form_row.block.name, 'value': form_row.value}
            yield form_row
            if 'form_fields' in form_row['value']:
                for field in form_row['value']['form_fields']:
                    field = field if is_lazy else {'type': field.block.name, 'value': field.value}
                    yield field


def form_get_email_fields(form):
    flat_fields = get_fields_flat(form)
    for field in flat_fields:
        if field['type'] == 'email':
            yield field


def get_variable_from_label(label):
    return get_slug_from_string(label).replace('-', '_')

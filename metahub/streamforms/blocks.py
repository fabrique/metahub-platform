from wagtail.core import blocks
from wagtailstreamforms.blocks import FormChooserBlock, WagtailFormBlock
#
# from metahub.streamforms.signals import post_process_form_instance
#
#
class FabriqueFormBlock(WagtailFormBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        # if parent_context and 'request' in parent_context:
        #     post_process_form_instance.send(
        #         sender=context['form'], request=parent_context['request'])
        return context


class FilteredFormChooserBlock(FormChooserBlock):
    """ Form chooser block that can filter the of forms that are choosable """

    def field(self):
        field = super().field
        field.queryset = getattr(self.target_model.objects, self.meta.instance_filter)()
        return field

    class Meta:
        instance_filter = 'multi_field'


class MailToAction(blocks.StructBlock):
    """ Helper block for stream forms to define where to mail to. """
    email_address = blocks.EmailBlock('Receiver')

    class Meta:
        label = 'Mail to action'

# from django.dispatch import Signal, receiver
# from wagtail.core.models import Site
# from wagtail.core.rich_text import RichText
#
# from qatar_museums.core.models import GlobalSettings
# from qatar_museums.extra_utils import make_richtext_links_external
#
# post_process_form_instance = Signal()
#
#
# @receiver(post_process_form_instance)
# def add_terms_and_conditions_text(sender, request, **kwargs):
#     """ We need the request to load the correct terms and conditions text """
#     if 'tac_checkbox' in sender.fields:
#         gs = GlobalSettings.for_site(Site.find_for_request(request))
#         sender.fields['tac_checkbox'].label = make_richtext_links_external(RichText(gs.tac_checkbox_text))

# from django.apps import AppConfig
# from django.conf import settings
# from django.db import IntegrityError, ProgrammingError
#
# from qatar_museums.mails.config import mails
#
#
# class MailAppConfig(AppConfig):
#     name = 'qatar_museums.mails'
#
#     def ready(self):
#         for key in mails:
#             from qatar_museums.mails.models import Mail
#             try:
#                 Mail.objects.get_or_create(key=key, defaults={
#                     'subject': 'QM e-ticket confirmation',
#                     'text': open(str(settings.APPS_DIR.path(f'mails/templates/mails/defaults/{key}.html')), 'r').read(),
#                 })
#             except (IntegrityError, ProgrammingError):
#                 pass

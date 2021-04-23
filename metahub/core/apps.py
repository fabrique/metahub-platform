from django.apps import AppConfig
from django.conf import settings

class CoreAppConfig(AppConfig):
    name = 'metahub.core'

    def ready(self):
        # import metahub.starling_metahub.filters
        # Custom devtools things!
        if 'devtools' in settings.INSTALLED_APPS:
            import deployment.config

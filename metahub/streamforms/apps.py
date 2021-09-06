from django.apps import AppConfig


class MetaHUBStreamformsAppConfig(AppConfig):
    name = 'metahub.streamforms'
    label = 'metahub_streamforms'

    def ready(self):
        import metahub.streamforms.signals

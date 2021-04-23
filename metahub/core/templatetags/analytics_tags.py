from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('core/components/google_tag_manager.html')
def google_tag_manager():
    return {
        'container_id': getattr(settings, 'GOOGLE_TAG_MANAGER_ID', ""),
    }


@register.inclusion_tag('core/components/google_tag_manager_noscript.html')
def google_tag_manager_noscript():
    return {
        'container_id': getattr(settings, 'GOOGLE_TAG_MANAGER_ID', ""),
    }

@register.inclusion_tag('core/components/matomo.html')
def matomo_script():
    return {
        'debug': getattr(settings, 'DEBUG', ""),
    }

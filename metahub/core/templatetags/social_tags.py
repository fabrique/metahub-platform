
from django.template import Library
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import stringfilter

from metahub.core.models import GlobalSettings


register = Library()


@register.simple_tag(takes_context=True)
def share_image(context):
    request = context['request']
    page = context.get('page')
    site = request.site

    share_image = page.get_share_image()
    if not share_image:
        share_image = GlobalSettings.for_site(site).default_share_image

    return share_image


@register.inclusion_tag('core/components/share.html', takes_context=True)
def share_buttons(context, url, title, image=None, hashtags='', show_pinterest=True):
    request = context['request']
    absolute_url = request.build_absolute_uri(url)
    return {
        'request': request,
        'url': absolute_url,
        'show_pinterest': show_pinterest,
        'twitter_text': _("tags.share.twitter_share_text{}").format(title),
        'twitter_hashtags': "metahub," + hashtags,
        'image': image,
        'title': title,
        'source': request.site.hostname,
        'mailto_subject': _("tags.share.mailto_subject{title}").format(title=title),
        'mailto_body': _("tags.share.mailto_body{url}").format(url=absolute_url),
    }

@register.filter
@stringfilter
def pinterest_fix(value):
    return value.replace('&', ' & ')


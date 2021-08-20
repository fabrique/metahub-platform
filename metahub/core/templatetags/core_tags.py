import random

from django import template

from django.utils.safestring import mark_safe

from wagtail.core.rich_text import RichText
from wagtail.core.rich_text import expand_db_html

from metahub.starling_metahub.structures.interfaces import StructureCookieBarRegular

register = template.Library()


@register.simple_tag
def absolute_uri(request, url=None):
    return request.build_absolute_uri(url)

@register.simple_tag
def absolute_uri_as(request, url=None):
    return request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page

@register.filter
def plain_richtext(value):
    """
    Rich text filter without the added rich text div.
    """
    if isinstance(value, RichText):
        # passing a RichText value through the |richtext filter should have no effect
        return value
    elif value is None:
        html = ''
    else:
        html = expand_db_html(value)
    return mark_safe(html)


@register.simple_tag
def randomhash():
    """
    Returns random id for use in templates.
    :return:
    """
    return '%08x' % random.randrange(16**8)

# from https://djangosnippets.org/snippets/545/
@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)

class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''

@register.simple_tag
def get_cookie_bar_component():
    return StructureCookieBarRegular()
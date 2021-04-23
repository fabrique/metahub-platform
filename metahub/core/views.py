from django.views import defaults as default_views
from django.views.generic import TemplateView


def bad_request(request, exception):
    return default_views.bad_request(request, exception, template_name='core/errors/400.html')


def permission_denied(request, exception):
    return default_views.permission_denied(request, exception, template_name='core/errors/403.html')


def page_not_found(request, exception):
    return default_views.page_not_found(request, exception, template_name='core/errors/404.html')


def server_error(request):
    return default_views.server_error(request, template_name='core/errors/500.html')


class FrontendTemplateView(TemplateView):
    """
    Simple class that renders (or tries to render) templates with the name
    given in the kwargs['template']
    If no value is given, it tries to render the index.html, which should
    contain an overview of all the templates available.
    """
    def get_template_names(self):
        template = self.kwargs.get('template')
        if template:
            return 'frontend/pages/{}.html'.format(template)
        return 'frontend/index.html'


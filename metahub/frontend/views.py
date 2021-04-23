from django.views.generic import TemplateView


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

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from metahub.core.models import MetahubBasePage


class MetaHubContentPage(MetahubBasePage):
    hero_header = StreamField([
    ])

    # CMS panels
    content = StreamField([

    ])

    content_panels = MetahubBasePage.content_panels + [
        StreamFieldPanel('hero_header'),
        StreamFieldPanel('content')
    ]
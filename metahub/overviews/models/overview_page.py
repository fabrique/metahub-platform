from starling.interfaces.generic import Resolution

from metahub.core.models import MetaHubBasePage


class MetaHubOverviewPage(MetaHubBasePage):
    parent_page_types = ['home.MetaHubMuseumSubHomePage']

    @property
    def cards(self):
        return [
            child.get_card_representation(Resolution('640x360'))
            for child in self.get_queryset()
        ]

    def get_queryset(self):
        """ What pages will show up on this overview """
        return self.get_children().live().specific()
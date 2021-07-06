from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Orderable, Site


class Menu(ClusterableModel):
    """
    Allows to build the site menu.
    """

    site = models.OneToOneField(
        Site, unique=True, db_index=True, on_delete=models.CASCADE)


    panels = [
        FieldPanel('site'),
        MultiFieldPanel([
            InlinePanel('menu_items'),
        ], heading='Items')
    ]

    def __str__(self):
        return str(self.site)

    @classmethod
    def for_site(cls, site):
        """
        Get an instance of this setting for the site.
        """
        instance, created = cls.objects.get_or_create(site=site)
        return instance

    def save(self, **kwargs):
        super().save(**kwargs)


class MenuItem(Orderable):
    """
    Item for a menu

    Items can have a certain type with a certain different behaviour.

    Items can have different behaviour for a different page. A dict
    with information based on page context can be created using the
    `for_page` method.
    """
    TYPE_PAGE = 'page'
    TYPE_DUMMY = 'custom'
    TYPE_CHOICES = (
        (TYPE_PAGE, 'Page'),
        (TYPE_DUMMY,'Custom'),
    )

    # CLASS_CHOICES = (
    #     ('', 'Normal'),
    #     ('__back-link','back link'),
    #     ('__favorites-link','favorites'),
    # )

    # ICON_CHOICES = (
    #     ('', 'None'),
    #     ('custom/ic_slash','slash'),
    #     ('custom/heart-icon','heart'),
    #     ('custom/ic_search', 'search')
    # )

    menu = ParentalKey('Menu', related_name='menu_items')

    link_type = models.CharField(
        'Type',
        max_length=15,
        choices=TYPE_CHOICES,
        default=TYPE_PAGE
    )

    link_title = models.CharField(
        'Title',
        max_length=63,
        blank=True
    )

    page = models.ForeignKey(
        'wagtailcore.Page', blank=True, null=True,
        verbose_name= 'Page', on_delete=models.CASCADE
    )

    custom_link_value = models.CharField(
        'Custom value',
        max_length=63,
        blank=True,
        help_text="Only needed for custom menu items"
    )

    # icon_before = models.CharField(
    #     'Icon before',
    #     max_length=25,
    #     choices=ICON_CHOICES,
    #     default='',
    #     blank=True
    # )
    # icon_after = models.CharField(
    #     'Icon after',
    #     max_length=25,
    #     choices=ICON_CHOICES,
    #     default='',
    #     blank=True
    # )

    panels = [
        FieldPanel('link_type'),
        FieldPanel('link_title'),
        PageChooserPanel('page'),
        FieldPanel('custom_link_value'),
        # FieldPanel('icon_before'),
        # FieldPanel('icon_after'),
    ]

    @property
    def url(self):
        if self.link_type == MenuItem.TYPE_DUMMY:
            return self.custom_link_value
        if self.link_type == MenuItem.TYPE_PAGE:
            return self.page.url
        raise NotImplementedError()

    def for_page(self, page):
        """
        Get menu item data based on current page context
        """
        url = self.url
        active = self.link_type == MenuItem.TYPE_PAGE and self.page and \
            (self.page.id == page.id or page.is_descendant_of(self.page))
        return {
            'active': active,
            'title': self.link_title,
            'url': url,
        }

    def __str__(self):
        return self.link_title

    class Meta(Orderable.Meta):
        pass

from django.db import models
from django.conf import settings


from django.forms.widgets import Textarea
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class PagePromoMixin(models.Model):
    """
    Adds extra items to the page promo tabs.

    Used for sharing, seo and when showing a link to the page somewhere else.
    Removes the default 'show_in_menus' option (use menus app instead)

    Separate mixin to keep related fields in one place
    """

    # promote
    promo_title = models.CharField(
        verbose_name='Promo titel',
        help_text="Optioneel, wordt getoond in plaats van titel als deze pagina op andere plekken gelinkt wordt",
        max_length=100,
        blank=True)

    promo_intro = models.TextField(
        verbose_name='Promo intro',
        help_text="Korte tekst die wordt getoond als deze pagina op andere plekken gelinkt wordt",
        blank=True)

    promo_link = models.CharField(
        verbose_name='Lees meer label',
        help_text="Tekst van het 'lees meer' linkje als deze pagina op andere plekken gelinkt wordt",
        max_length=50,
        blank=True)

    promo_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        verbose_name='Promo afbeelding',
        null=True,
        blank=True,
        help_text="Optioneel, wordt getoond als deze pagina op andere plekken gelinkt wordt",
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # share
    share_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        verbose_name='Share afbeelding',
        null=True,
        blank=True,
        help_text="Optioneel, anders wordt promo afbeelding gebruikt, anders de pagina visual en anders de standaard deel afbeelding",
        on_delete=models.SET_NULL,
        related_name='+'
    )

    twitter_hashtags = models.CharField(
        verbose_name='Twitter hashtags',
        help_text='Commagescheiden lijst van termen die als hashtag worden toegevoegd wanneer gedeeld op twitter, zonder de #',
        blank=True,
        max_length=100
    )

    seo_panel = MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], 'Search & SEO')

    promo_panel_fields = [
        FieldPanel('promo_title', widget=Textarea(attrs={'rows': 2})),
        FieldPanel('promo_intro'),
        FieldPanel('promo_link'),
        ImageChooserPanel('promo_image')]
    promo_panel = MultiFieldPanel(promo_panel_fields, 'Pagina promo opties')

    share_panel = MultiFieldPanel([
            ImageChooserPanel('share_image'),
            FieldPanel('twitter_hashtags'),
        ], 'Extra sharing opties')

    promote_panels = [
        seo_panel,
        promo_panel,
        share_panel, ]

    promote_tab = ObjectList(promote_panels, heading='Promote')

    def get_promo_image(self):
        if self.promo_image:
            return self.promo_image

    def get_promo_title(self):
        if self.promo_title:
            return self.promo_title
        return self.title

    def get_share_image(self):
        if self.share_image:
            return self.share_image
        return self.get_promo_image()

    def get_page_description(self):
        if self.search_description:
            return self.search_description
        return self.get_promo_intro()

    def get_promo_intro(self):
        return self.promo_intro

    class Meta:
        abstract = True


class PageIntroMixin(models.Model):
    page_intro = models.TextField('Paginaintro', blank=True)

    def get_promo_intro(self):
        promo_intro = super().get_promo_intro()
        if not promo_intro:
            promo_intro = self.page_intro
        return promo_intro

    class Meta:
        abstract = True


class PageVisualMixin(models.Model):
    """
    Base page for pages with a single page visual
    """
    page_visual = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=False,
        verbose_name='Pagina afbeelding',
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_promo_image(self):
        # use page visual if no explicit promo image
        # also used as fallback for share image
        promo_image = super().get_promo_image()
        if not promo_image:
            promo_image = self.page_visual
        return promo_image

    class Meta:
        abstract = True


class SinglePagePerSiteMixin:

    @classmethod
    def can_create_at(cls, parent):
        can_create_at = super().can_create_at(parent)
        # import pdb;pdb.set_trace()
        if can_create_at:
            # check there is no such page yet for the site
            return not parent.get_root().get_descendants().type(cls).exists()
        return False

    @classmethod
    def get_for_site(cls, site):
        return site.root_page.get_descendants().type(cls).first()



from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmodelchooser import register_model_chooser


class AbstractPerson(models.Model):
    """ Abstract base model to be able to reuse people for different stuff """

    name = models.CharField(_('Name'), blank=True, max_length=127)
    title = models.CharField(_('Title/Role/Responsibility'), blank=True, max_length=127)
    # museum = models.CharField()
    # avatar = models.ForeignKey(
    #     settings.WAGTAILIMAGES_IMAGE_MODEL,
    #     verbose_name=_('Avatar'),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        # ImageChooserPanel('avatar'),
    ]

    # def get_avatar(self):
    #     if self.avatar:
    #         return self.avatar
    #     # TODO: Peoplesetting is abstract, so you can't use that
    #     # TODO: but it feels bad to refer to a non abstract class since
    #     # TODO: this method is defined within an abstract class?
    #     # TODO: solution, move this implementation to subclass and
    #     # TODO: put NotImplemented here?
    #     return ContactPersonSetting.for_site(self.site).get_default_person_avatar()
    #
    # def get_starlized_avatar(self):
    #     return AtomPictureRegular(**Resolution(mobile='200', crop=True).resolve(self.get_avatar()))

    # def get_card_data(self, custom_title=None):
    #     return MoleculePersonRegular(
    #         name=self.name,
    #         title=custom_title if custom_title else self.title,
    #     )

    def __str__(self):
        return self.name

    # Override save and set site

    class Meta:
        abstract = True


@register_model_chooser
class Author(AbstractPerson):
    """ Author of news, story etc """

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
from django.db import models


class CollectionCategory(models.Model):
    """
    Represents the different areas of the MetaHub collection, such as Objekt, Objektseries,
    Geschichten etc. A Story/Object/Series page belongs to one of these categories.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paginacategorie'
        verbose_name_plural = 'Paginacategorieen'
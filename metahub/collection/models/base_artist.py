from django.db import models


class BaseCollectionArtist(models.Model):
    """
    Artist model based on the data from BeeCollect. Properties that are important
    to BeeCollect only are preceded by bc. Objects can be related to 1 Artist only.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    bc_inventory_number = models.CharField(max_length=1024)
    bc_date_acquired = models.CharField(max_length=256)
    bc_change_user = models.CharField(max_length=256)
    bc_change_date = models.CharField(max_length=256)
    bc_dating = models.CharField(max_length=256)

    type = models.CharField(max_length=256)
    first_name = models.CharField(max_length=1024, default='')
    last_name = models.CharField(max_length=1024, default='')
    alias_name = models.CharField(max_length=1024, default='')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
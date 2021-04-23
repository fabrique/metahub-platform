from django.db import models

class BeeCollectSyncOccurrence(models.Model):
    date_done = models.DateTimeField(auto_now_add=True)
    date_data_dump = models.CharField(max_length=1000)
    success = models.BooleanField(default=False)

    objects_in_dump = models.PositiveIntegerField(default=0)
    objects_added = models.PositiveIntegerField(default=0)
    objects_changed = models.PositiveIntegerField(default=0)
    objects_removed = models.PositiveIntegerField(default=0)

    artists_in_dump = models.PositiveIntegerField(default=0)
    artists_added = models.PositiveIntegerField(default=0)
    artists_changed = models.PositiveIntegerField(default=0)
    artists_removed = models.PositiveIntegerField(default=0)


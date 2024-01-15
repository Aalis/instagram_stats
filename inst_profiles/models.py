from django.db import models


class InstProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    link = models.URLField(unique=True)
    followers_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

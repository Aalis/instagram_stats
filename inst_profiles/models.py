from django.db import models


class InstProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    link = models.URLField()
    followers_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

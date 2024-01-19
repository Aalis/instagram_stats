from django.db import models
from users.models import CustomUser


class InstProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    link = models.URLField(unique=True)
    followers_count = models.PositiveIntegerField(blank=True, null=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,  # You can adjust this based on your requirements
        blank=True,
    )

    def __str__(self):
        return self.name

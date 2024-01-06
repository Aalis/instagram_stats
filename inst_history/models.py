from django.db import models
from inst_profiles.models import InstProfile


class InstHistory(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(InstProfile, on_delete=models.CASCADE)
    followers_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

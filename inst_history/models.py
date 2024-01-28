from django.db import models
from django.utils import timezone
from inst_profiles.models import InstProfile


class InstHistory(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(InstProfile, on_delete=models.CASCADE)
    followers_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def followers_subscribed_last_24_hours(self):
        # Calculate the datetime 24 hours ago
        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)

        # Get the two most recent InstHistory records for the profile created in the last 24 hours
        last_24_hours_history = InstHistory.objects.filter(
            profile=self.profile, created_at__gte=twenty_four_hours_ago
        ).order_by("-created_at")[:2]

        # Calculate the difference in followers_count
        if len(last_24_hours_history) == 2:
            initial_followers_count = last_24_hours_history[1].followers_count
            final_followers_count = last_24_hours_history[0].followers_count
            return final_followers_count - initial_followers_count

        return 0

from django import forms
from .models import InstProfile


class InstProfileForm(forms.ModelForm):
    class Meta:
        model = InstProfile
        fields = ["name", "link", "followers_count"]

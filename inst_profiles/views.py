from django.shortcuts import render, redirect
from .models import InstProfile
from .forms import InstProfileForm
from .tasks import celery_task
from instagram_stats.celery import plus
from bs4 import BeautifulSoup
import requests


def add_instprofile(request):
    celery_task.apply_async(countdown=10)
    if request.method == "POST":
        form = InstProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("instprofile_list")

    else:
        form = InstProfileForm()
    return render(request, "add_instprofile.html", {"form": form})


def instprofile_list(request):
    inst_profiles = InstProfile.objects.all()
    return render(request, "instprofile_list.html", {"inst_profiles": inst_profiles})


def parse_instagram(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, "lxml")
    followers_count = soup.find("span", class_="_ac2a")["title"]
    print(f"Followers Count: {followers_count}")

from django.shortcuts import render, redirect
from .models import InstProfile
from .forms import InstProfileForm


def add_instprofile(request):
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

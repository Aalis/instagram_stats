from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin  # Import LoginRequiredMixin
from .models import InstProfile
from .forms import InstProfileForm
from .tasks import get_followers_count


class InstProfileListView(LoginRequiredMixin, ListView):
    model = InstProfile
    template_name = "instprofile_list.html"
    login_url = "home"  # Specify your login URL

    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        return InstProfile.objects.filter(user=self.request.user)


class InstProfileCreateView(CreateView):
    model = InstProfile
    form_class = InstProfileForm
    template_name = "add_instprofile.html"
    success_url = reverse_lazy("instprofile_list")  # Redirect to list view on success

    def form_valid(self, form):
        # Set the user before saving the form
        form.instance.user = self.request.user

        # Access the link value from the form data
        link = form.cleaned_data["link"]

        # Call Celery task with the link value
        get_followers_count.delay(link)

        # Continue with the form validation and saving
        return super().form_valid(form)


class InstProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = InstProfile
    template_name = "instprofile_confirm_delete.html"
    success_url = reverse_lazy("instprofile_list")

    def get_object(self, queryset=None):
        return get_object_or_404(InstProfile, pk=self.kwargs["pk"])

    def get_queryset(self):
        # Filter the queryset based on the logged-in user
        return InstProfile.objects.filter(user=self.request.user)

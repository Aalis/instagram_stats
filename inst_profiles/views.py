from django.views.generic import CreateView, ListView
from .models import InstProfile
from .forms import InstProfileForm
from .tasks import celery_task


class InstProfileListView(ListView):
    model = InstProfile
    template_name = "instprofile_list.html"


class InstProfileCreateView(CreateView):
    model = InstProfile
    form_class = InstProfileForm
    template_name = "add_instprofile.html"
    success_url = "/inst_profiles/"  # Redirect to list view on success

    def form_valid(self, form):
        profile_url = form.cleaned_data[
            "link"
        ]  # Assuming the link field in your form is named 'link'
        celery_task.apply_async(
            args=[profile_url], countdown=5
        )  # Pass the profile URL as an argument
        return super().form_valid(form)

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
        celery_task.apply_async(countdown=5)  # Call Celery task before saving
        return super().form_valid(form)


# def parse_instagram(link):
#     html_text = requests.get(link).text
#     soup = BeautifulSoup(html_text, "lxml")
#     followers_count = soup.find("span", class_="_ac2a")["title"]
#     print(f"Followers Count: {followers_count}")

from django.urls import path
from .views import InstProfileListView, InstProfileCreateView

urlpatterns = [
    path("", InstProfileListView.as_view(), name="instprofile_list"),
    path("add/", InstProfileCreateView.as_view(), name="add_instprofile"),
]

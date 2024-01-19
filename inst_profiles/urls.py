from django.urls import path
from .views import InstProfileListView, InstProfileCreateView, InstProfileDeleteView

urlpatterns = [
    path("", InstProfileListView.as_view(), name="instprofile_list"),
    path(
        "delete/<int:pk>/", InstProfileDeleteView.as_view(), name="delete_instprofile"
    ),
    path("add/", InstProfileCreateView.as_view(), name="add_instprofile"),
]

from django.urls import path
from .views import instprofile_history

urlpatterns = [
    path(
        "instprofile/<int:profile_id>/history/",
        instprofile_history,
        name="instprofile_history",
    ),
]

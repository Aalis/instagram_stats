from .views import add_instprofile, instprofile_list
from django.urls import path

urlpatterns = [
    path("add/", add_instprofile, name="add_instprofile"),
    path("list/", instprofile_list, name="instprofile_list"),
]

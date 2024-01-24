# inst_profiles/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import InstProfile


class InstProfileViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        self.inst_profile = InstProfile.objects.create(
            name="Test Profile",
            link="http://example.com",
            followers_count=100,
            user=self.user,
        )

    def test_inst_profile_list_view(self):
        response = self.client.get(reverse("instprofile_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "instprofile_list.html")
        self.assertIn(self.inst_profile, response.context["object_list"])

    def test_inst_profile_create_view(self):
        response = self.client.get(reverse("add_instprofile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_instprofile.html")

        response = self.client.post(
            reverse("add_instprofile"),
            {
                "name": "New Profile",
                "link": "http://newexample.com",
                "followers_count": 50,
            },
        )
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertEqual(InstProfile.objects.filter(name="New Profile").count(), 1)

    def test_inst_profile_delete_view(self):
        response = self.client.get(
            reverse("delete_instprofile", kwargs={"pk": self.inst_profile.pk})
        )
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

        response = self.client.post(
            reverse("delete_instprofile", kwargs={"pk": self.inst_profile.pk})
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertFalse(InstProfile.objects.filter(pk=self.inst_profile.pk).exists())

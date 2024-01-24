from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


class SignUpViewTest(TestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")

    def test_signup_form_submission(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "age": 25,
        }

        response = self.client.post(self.signup_url, data, follow=True)
        self.assertRedirects(response, self.login_url, target_status_code=200)

        # Check that the user is now logged in
        user = get_user_model().objects.get(email="test@example.com")
        self.assertTrue(user.is_authenticated)

    def test_signup_redirects_to_login(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "age": 25,
        }

        response = self.client.post(self.signup_url, data, follow=True)

        self.assertRedirects(response, self.login_url, target_status_code=200)

        # Check that the user is now logged in
        user = get_user_model().objects.get(email="test@example.com")
        self.assertTrue(user.is_authenticated)

    def test_signup_failure(self):
        data = {
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "wrongpassword",  # Mismatched password
            "first_name": "Test",
            "last_name": "User",
            "age": 25,
        }

        response = self.client.post(self.signup_url, data, follow=True)

        # Check for the specific form error for the 'password2' field
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        # Update this line to match the actual error message
        self.assertIn(
            "there was an error creating your account. please try again.",
            messages[0].message.lower(),
        )
        self.assertEqual(messages[0].tags, "error")

from django.test import TestCase
from django.urls import reverse


class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/signup/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("account_signup"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")


class LogInPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/login/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_view_name(self):
        response = self.client.get(reverse("account_login"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

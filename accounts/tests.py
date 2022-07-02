from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/signup/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("account_signup"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_signup_form_full(self):
        response = self.client.post(
            reverse("account_signup"),
            {
                "first_name": "Firstname",
                "last_name": "Lastname",
                "email": "email@email.com",
                "password1": "password123!",
                "password2": "password123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].first_name, "Firstname")
        self.assertEqual(get_user_model().objects.all()[0].last_name, "Lastname")
        self.assertEqual(get_user_model().objects.all()[0].email, "email@email.com")

    def test_signup_form_wo_name(self):
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "email@email.com",
                "password1": "password123!",
                "password2": "password123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].first_name, "")
        self.assertEqual(get_user_model().objects.all()[0].last_name, "")
        self.assertEqual(get_user_model().objects.all()[0].email, "email@email.com")


class LogInPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/login/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_view_name(self):
        response = self.client.get(reverse("account_login"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_login(self):
        # TODO: change this not use use signup page
        self.client.post(
            reverse("account_signup"),
            {
                "email": "email@email.com",
                "password1": "password123!",
                "password2": "password123!",
            },
        )
        response = self.client.post(
            reverse("account_login"),
            {"login": "email@email.com", "password": "password123!"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_active)

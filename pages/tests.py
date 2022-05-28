from django.test import SimpleTestCase
from django.urls import reverse


class FaviconTests(SimpleTestCase):
    def test_get_requests(self):
        response = self.client.get("/favicon.ico")
        print(response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "max-age=86400, immutable, public")
        self.assertEqual(response["Content-Type"], "image/vnd.microsoft.icon")
        self.assertGreaterEqual(len(response.getvalue()), 0)


class HomePageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")


class AboutPageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")


class FaqPageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/faq")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("faq"))
        self.assertTemplateUsed(response, "faq.html")

import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Event, Choice


class NewEventPageTests(TestCase):
    def setUp(self):
        # TODO: consider testing dynamic formset with Selenium
        self.client.force_login(
            get_user_model().objects.get_or_create(username="testuser")[0]
        )
        self.test_event_data = {
            "event_name": "New Test Event",
            "password_protect": True,
            "password": "eventpassword",
            "allow_add": True,
            "form-0-time_from": "01/01/2022",
            "form-0-time_to": "02/01/2022",
            "form-1-time_from": "03/01/2022",
            "form-1-time_to": "04/02/2022",
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 1000,
        }

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/events/create_event")
        self.assertEqual(response.status_code, 200)

    def test_newevent_view_name(self):
        response = self.client.get(reverse("create_event"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "new_event.html")

    def test_create_new_form(self):
        response = self.client.post(reverse("create_event"), self.test_event_data)

        self.assertEqual(response.status_code, 302)  # test form success redirect

        # test form creation content
        self.assertEqual(Event.objects.last().event_name, "New Test Event")
        self.assertTrue(Event.objects.last().password_protect)
        self.assertIsNotNone(Event.objects.last().password)
        self.assertTrue(Event.objects.last().allow_add)

        # test Choice model
        choice_model_obj = Choice.objects.filter(event_id=Event.objects.last().id)
        self.assertEqual(choice_model_obj.count(), 2)
        self.assertTrue(isinstance)
        for i in range(2):
            self.assertTrue(
                isinstance(choice_model_obj[i].time_from, datetime.datetime)
            )
            self.assertTrue(isinstance(choice_model_obj[i].time_to, datetime.datetime))

import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Attendee, Event, Choice, AttendeeChoice


class EventsModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username",
            email="username@email.com",
            password="password",
        )
        self.event = Event.objects.create(
            user_id=self.user,
            event_name="eventname",
            event_description="event description",
            allow_add=True,
            password_protect=True,
            password="eventpw",
        )
        self.choice = Choice.objects.create(
            time_from=datetime.datetime(2020, 1, 2, 1, 0, tzinfo=datetime.timezone.utc),
            time_to=datetime.datetime(2020, 1, 2, 2, 0, tzinfo=datetime.timezone.utc),
            event_id=self.event,
        )
        self.attendee = Attendee.objects.create(
            name="votername",
            event_id=self.event,
        )
        self.attendeechoice = AttendeeChoice.objects.create(
            status=1,
            attendee_id=self.attendee,
            choice_id=self.choice,
        )

    def test_event_model(self):
        self.assertEqual(self.event.user_id, self.user)
        self.assertEqual(self.event.event_name, "eventname")
        self.assertEqual(self.event.event_description, "event description")
        self.assertTrue(self.event.allow_add)
        self.assertTrue(self.event.password_protect)
        self.assertEqual(str(self.event), "eventname")

    def test_choice_model(self):
        self.assertEqual(
            self.choice.time_from,
            datetime.datetime(2020, 1, 2, 1, 0, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(
            self.choice.time_to,
            datetime.datetime(2020, 1, 2, 2, 0, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(self.choice.event_id, self.event)
        self.assertEqual(str(self.choice), "event_eventname_choice")

    def test_attendee_model(self):
        self.assertEqual(self.attendee.name, "votername")
        self.assertEqual(self.attendee.event_id, self.event)
        self.assertEqual(str(self.attendee), "votername")

    def test_attendee_choice_model(self):
        self.assertEqual(self.attendeechoice.status, 1)
        self.assertEqual(self.attendeechoice.attendee_id, self.attendee)
        self.assertEqual(self.attendeechoice.choice_id, self.choice)
        self.assertEqual(str(self.attendeechoice), str(self.attendee))


class NewEventPageTests(TestCase):
    def setUp(self):
        # TODO: consider testing dynamic formset with Selenium
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(self.new_user)

        self.test_event_data = {
            "event_name": "New Test Event",
            "password_protect": True,
            "password": "eventpassword",
            "allow_add": True,
            "form-0-time_from": "01/01/2022",
            "form-0-time_to": "02/01/2022",
            "form-1-time_from": "03/01/2022 01:00",
            "form-1-time_to": "04/02/2022 02:00",
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
        self.assertEqual(str(Event.objects.last().user_id), self.new_user.email)

        # test Choice model
        choice_model_obj = Choice.objects.filter(event_id=Event.objects.last().id)
        self.assertEqual(choice_model_obj.count(), 2)
        self.assertTrue(isinstance)
        for i in range(2):
            self.assertTrue(
                isinstance(choice_model_obj[i].time_from, datetime.datetime)
            )
            self.assertTrue(isinstance(choice_model_obj[i].time_to, datetime.datetime))


class NewEventSuccessTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(new_user)
        self.new_event = Event.objects.create(event_name="New Event", user_id=new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/success/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("success", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "new_event_success.html")


class LoggedInEventVoteTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(new_user)
        self.new_event = Event.objects.create(
            event_name="New Event", user_id=new_user, password_protect=True
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/vote/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("vote", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vote.html")


class AnonEventVoteTest(TestCase):
    def test_no_password_protection(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event", user_id=new_user, password_protect=False
        )

        response = self.client.get(
            f"/events/vote/{self.new_event.access_link}", follow=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vote.html")

    def test_password_protected_view_no_session(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event", user_id=new_user, password_protect=True
        )

        response = self.client.get(
            f"/events/vote/{self.new_event.access_link}", follow=False
        )
        self.assertEqual(response.status_code, 302)

    def test_password_protected_view_with_session(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event", user_id=new_user, password_protect=True
        )

        session = self.client.session
        session[f"unlock-{self.new_event.access_link}"] = True
        session.save()

        response = self.client.get(
            f"/events/vote/{self.new_event.access_link}", follow=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vote.html")


class VoteViewSubmissionTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event", user_id=new_user, password_protect=True
        )
        self.new_choice_first = Choice.objects.create(
            event_id=self.new_event,
            time_from=datetime.datetime(2020, 1, 2, 1, 0, tzinfo=datetime.timezone.utc),
            time_to=datetime.datetime(2020, 1, 2, 2, 0, tzinfo=datetime.timezone.utc),
        )
        self.new_choice_sec = Choice.objects.create(
            event_id=self.new_event,
            time_from=datetime.datetime(2020, 1, 2, 3, 0, tzinfo=datetime.timezone.utc),
            time_to=datetime.datetime(2020, 1, 2, 4, 0, tzinfo=datetime.timezone.utc),
        )

    def test_vote(self):
        session = self.client.session
        session[f"unlock-{self.new_event.access_link}"] = True
        session.save()

        request = self.client.post(
            reverse("vote", args=[self.new_event.access_link]),
            {
                "name": "First Last",
                "form-0-status": 2,
                "form-1-status": 1,
                "form-TOTAL_FORMS": 2,
                "form-INITIAL_FORMS": 0,
                "form-MIN_NUM_FORMS": 0,
                "form-MAX_NUM_FORMS": 1000,
                "choice-id": [self.new_choice_first.pk, self.new_choice_sec.pk],
                "event-uuid": str(self.new_event.access_link),
            },
        )

        self.assertEqual(Attendee.objects.last().name, "First Last")
        self.assertEqual(AttendeeChoice.objects.count(), 2)
        self.assertEqual(AttendeeChoice.objects.all()[0].status, 2)
        self.assertEqual(AttendeeChoice.objects.all()[1].status, 1)
        self.assertTrue(
            AttendeeChoice.objects.all()[0].attendee_id.name
            == Attendee.objects.last().name
        )
        self.assertTrue(
            AttendeeChoice.objects.all()[1].attendee_id.name
            == Attendee.objects.last().name
        )
        self.assertTrue(
            AttendeeChoice.objects.all()[0].choice_id.pk == Choice.objects.all()[0].pk
        )
        self.assertTrue(
            AttendeeChoice.objects.all()[1].choice_id.pk == Choice.objects.all()[1].pk
        )


class VoteUnlockTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/unlock/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("unlock", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "unlock_vote.html")

    def test_logged_in_redirect(self):
        self.client.force_login(self.new_user)
        response = self.client.get(
            reverse("unlock", args=[self.new_event.access_link]), follow=False
        )
        self.assertEqual(response.status_code, 302)

    def test_unlock_session_redirect(self):
        session = self.client.session
        session[f"unlock-{self.new_event.access_link}"] = True
        session.save()

        response = self.client.get(
            reverse("unlock", args=[self.new_event.access_link]), follow=False
        )
        self.assertEqual(response.status_code, 302)


class VoteAddTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )
        self.client.force_login(self.new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/add/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("add", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vote_add.html")

    def test_add_new_time(self):
        test_data = {
            "form-0-time_from": "01/01/2022",
            "form-0-time_to": "02/01/2022",
            "event": self.new_event.access_link,
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 1000,
        }
        response = self.client.post(
            reverse("add", args=[self.new_event.access_link]), test_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Choice.objects.last().time_from,
            datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        )


class DashboardViewTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )
        self.client.force_login(self.new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/events/dashboard", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_event_in_list(self):
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertContains(response, "New Event")


class EventDetailViewTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )
        self.client.force_login(self.new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get(f"/events/{self.new_event.access_link}", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_detail.html")

    def test_event_in_title(self):
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertContains(response, "New Event")

    def test_user_permissions(self):
        self.client.logout()
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertTemplateUsed(response, "account/login.html")

        credentials = {
            "username": "email2",
            "email": "email2@email.com",
            "password": "password123!",
        }
        diff_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(diff_user)
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 403)


class EventDeleteViewTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )
        self.client.force_login(self.new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/delete/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("delete", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_event.html")

    def test_event_deleted(self):
        response = self.client.post(
            reverse("delete", args=[self.new_event.access_link])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)

    def test_user_permissions(self):
        self.client.logout()
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertTemplateUsed(response, "account/login.html")

        credentials = {
            "username": "email2",
            "email": "email2@email.com",
            "password": "password123!",
        }
        diff_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(diff_user)
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 403)


class ChoiceDeleteViewTests(TestCase):
    def setUp(self):
        credentials = {
            "username": "email",
            "email": "email@email.com",
            "password": "password123!",
        }
        self.new_user = get_user_model().objects.create_user(**credentials)
        self.new_event = Event.objects.create(
            event_name="New Event",
            user_id=self.new_user,
            password_protect=True,
            password="password",
        )
        self.new_choice = Choice.objects.create(
            time_from=datetime.datetime(2020, 1, 2, 1, 0, tzinfo=datetime.timezone.utc),
            time_to=datetime.datetime(2020, 1, 2, 2, 0, tzinfo=datetime.timezone.utc),
            event_id=self.new_event,
        )
        self.client.force_login(self.new_user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get(
            f"/events/delete_choice/{self.new_event.access_link}", follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_name(self):
        response = self.client.get(
            reverse("delete_choice", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vote_delete.html")

    def test_delete_choice(self):
        response = self.client.post(
            reverse("delete_choice", args=[self.new_event.access_link]),
            {
                self.new_choice.pk: "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Choice.objects.count(), 0)

    def test_user_permissions(self):
        self.client.logout()
        response = self.client.get(
            reverse("delete_choice", args=[self.new_event.access_link]), follow=True
        )
        self.assertTemplateUsed(response, "account/login.html")

        credentials = {
            "username": "email2",
            "email": "email2@email.com",
            "password": "password123!",
        }
        diff_user = get_user_model().objects.create_user(**credentials)
        self.client.force_login(diff_user)
        response = self.client.get(
            reverse("event", args=[self.new_event.access_link]), follow=True
        )
        self.assertEqual(response.status_code, 403)

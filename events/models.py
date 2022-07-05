from telnetlib import STATUS
import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings


class Event(models.Model):
    access_link = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    event_name = models.CharField(max_length=128)
    event_description = models.TextField(max_length=512, default="", blank=True)
    allow_add = models.BooleanField(default=False)
    password_protect = models.BooleanField(default=False)
    password = models.CharField(max_length=32, default="", blank=True)

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.access_link)])


class Choice(models.Model):
    time_from = models.DateTimeField(null=False)
    time_to = models.DateTimeField(null=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"event_{self.event_id}_choice"


class Attendee(models.Model):
    name = models.CharField(max_length=64, null=False)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)


class AttendeeChoice(models.Model):
    YES = 1
    MAYBE = 2
    NO = 3
    STATUS = (
        (YES, "Yes"),
        (MAYBE, "Maybe"),        
        (NO, "No"),
    )

    attendee_id = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Choice, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS)
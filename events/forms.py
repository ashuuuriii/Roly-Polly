from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

from .models import Event, Choice


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["user_id"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        event = super(NewEventForm, self).save(commit=False)
        event.password = make_password(self.cleaned_data["password"])
        if commit:
            event.save()
        return event


class ChoiceForm(forms.ModelForm):
    # TODO: add validation to prevent users from inputting past dates or duplicates
    time_from = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M", "%d/%m/%Y"])
    time_to = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M", "%d/%m/%Y"])


# use formset factory to create dynamic fields
ChoiceFormset = forms.modelformset_factory(
    Choice, form=ChoiceForm, fields=["time_from", "time_to"], extra=1, can_delete=True
)


class UnlockVoteForm(forms.Form):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_password(self):
        # cannot be tested because test case creates a separate blank db
        uuid_slug = self.data.get("event_id")
        entered_pw = self.data.get("password")
        event_pw = Event.objects.get(access_link=uuid_slug).password
        if not check_password(entered_pw, event_pw):
            raise ValidationError("You have not entered the correct password.")

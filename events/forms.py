from django import forms
from django.contrib.auth.hashers import make_password

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
    time_from = forms.DateTimeField(input_formats=["%d/%m/%Y"])
    time_to = forms.DateTimeField(input_formats=["%d/%m/%Y"])


# use formset factory to create dynamic fields
ChoiceFormset = forms.modelformset_factory(
    Choice, form=ChoiceForm, fields=["time_from", "time_to"], extra=1, can_delete=True
)

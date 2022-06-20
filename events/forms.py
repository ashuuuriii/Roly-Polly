from django.forms import ModelForm, modelformset_factory, DateTimeField

from .models import Event, Choice


class NewEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['user_id']


class ChoiceForm(ModelForm):
    # TODO: add validation to prevent users from inputting past dates
    time_from = DateTimeField(input_formats=["%d/%m/%Y"])
    time_to = DateTimeField(input_formats=["%d/%m/%Y"])


# use formset factory to create dynamic fields
ChoiceFormset = modelformset_factory(
    Choice, form=ChoiceForm, fields=["time_from", "time_to"], extra=1
)

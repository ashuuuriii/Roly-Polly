from django import forms


class NewEventForm(forms.Form):
    event_name = forms.CharField(label="Event Name", max_length=160)
    event_description = forms.CharField(
        label="Event Description", widget=forms.Textarea, required=False, max_length=360
    )
    allow_new_answers = forms.ChoiceField(
        label="Allow users to add new dates?",
        choices=[(True, "Yes"), (False, "No")],
        widget=forms.RadioSelect,
    )
    password = forms.BooleanField(
        label="Set password?", widget=forms.PasswordInput, required=False
    )

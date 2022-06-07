from django.views.generic.edit import FormView
from .forms import NewEventForm


class NewEventFormView(FormView):
    template_name = 'new_event.html'
    form_class = NewEventForm
    # success_url = '/saved/'yy
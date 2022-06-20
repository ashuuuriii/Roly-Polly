from django.shortcuts import render

from .forms import NewEventForm, ChoiceFormset
from .models import Choice


def new_event_view(request):
    template_name = "new_event.html"
    if request.method == "GET":
        event_form = NewEventForm(request.GET or None)
        choice_formset = ChoiceFormset(queryset=Choice.objects.none())
    elif request.method == "POST":
        event_form = NewEventForm(request.POST)
        choice_formset = ChoiceFormset(request.POST)
        if event_form.is_valid() and choice_formset.is_valid():
            event = event_form.save(commit=False)
            event.user_id = request.user
            event.save()
            for formset in choice_formset:
                choice = formset.save(commit=False)
                choice.event_id = event
                choice.save()
            choice_formset.save()
        # TODO: redirect to success page

    return render(
        request,
        template_name,
        {"event_form": event_form, "choice_form": choice_formset},
    )

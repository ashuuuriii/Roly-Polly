from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NewEventForm, ChoiceFormset, UnlockVoteForm
from .models import Choice


@login_required
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
                # TODO: Check if this is proper usage.
                # ModelFormSet should remove forms marked as delete by default
                if formset.cleaned_data.get("DELETE"):
                    continue
                choice = formset.save(commit=False)
                choice.event_id = event
                choice.save()
            choice_formset.save()
            return redirect("success", uuid_slug=event.access_link)

    return render(
        request,
        template_name,
        {"event_form": event_form, "choice_form": choice_formset},
    )


class NewEventSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "new_event_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_view_link"] = reverse(
            "vote", kwargs={"uuid_slug": context.get("uuid_slug")}
        )
        return context


class EventVoteView(TemplateView):
    template_name = "vote.html"


class UnlockVoteView(TemplateView):
    template_name = "unlock_vote.html"

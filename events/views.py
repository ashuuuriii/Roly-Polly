from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NewEventForm, ChoiceFormset, UnlockVoteForm
from .models import Choice, Event


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


class EventVoteView(DetailView):
    template_name = "vote.html"
    model = Event
    slug_url_kwarg = "uuid_slug"
    slug_field = "access_link"

    def get(self, request, *args, **kwargs):
        # makes the uuid slug available within context
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, **kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """
        checks if the user is the user creator, has already entered the password
        or if the event is password protected.
        """
        uuid = context.get("uuid_slug")
        password_protect = context.get("event").password_protect
        event_user = str(context.get("event").user_id)
        current_user = self.request.user.email if self.request.user.id else None

        if (
            self.request.session.get(f"unlock-{uuid}")
            or not password_protect
            or (event_user == current_user)
        ):
            return super().render_to_response(context, **response_kwargs)
        else:
            return redirect("unlock", uuid_slug=uuid)


class UnlockVoteView(FormView):
    template_name = "unlock_vote.html"
    form_class = UnlockVoteForm

    def get(self, request, *args, **kwargs):
        # makes the uuid slug available within context
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid_slug"] = kwargs.get("uuid_slug")
        context["event_data"] = Event.objects.get(access_link=context["uuid_slug"])
        return context

    def render_to_response(self, context, **response_kwargs):
        uuid = context.get("uuid_slug")
        event_user = str(context.get("event_data").user_id)
        password_protect = context.get("event_data").password_protect
        current_user = self.request.user.email if self.request.user.id else None

        if (
            self.request.session.get(f"unlock-{uuid}")
            or not password_protect
            or (event_user == current_user)
        ):
            return redirect("vote", uuid_slug=uuid)
        else:
            return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        """
        password checking is implemented within the form"s clean_password
        method.
        """
        uuid_slug = form.data.get("event_id")
        self.request.session[f"unlock-{uuid_slug}"] = True
        return redirect("vote", uuid_slug=uuid_slug)

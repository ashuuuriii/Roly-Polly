from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    FormView,
    DetailView,
    ListView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.core.exceptions import PermissionDenied

from .forms import (
    NewEventForm,
    ChoiceFormset,
    UnlockVoteForm,
    AttendeeForm,
    ChoiceVoteForm,
    ChoiceVoteBaseFormset,
)
from .models import Choice, Event, AttendeeChoice


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
            if event_form.data.get('password'):
                event.password_protect = True
            if request.user.is_authenticated:
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


class NewEventSuccessView(TemplateView):
    template_name = "new_event_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_view_link"] = reverse(
            "vote", kwargs={"uuid_slug": context.get("uuid_slug")}
        )
        return context


class EventVoteView(UserPassesTestMixin, DetailView):
    template_name = "vote.html"
    model = Event
    slug_url_kwarg = "uuid_slug"
    slug_field = "access_link"
    attendee_form_class = AttendeeForm
    choice_form_class = ChoiceVoteForm

    def get(self, request, *args, **kwargs):
        # makes the uuid slug available within context
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, attendee_form=None, vote_form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choices"] = Choice.objects.filter(event_id=context["object"].pk)
        context["attendee_form"] = (
            self.attendee_form_class() if not attendee_form else attendee_form
        )
        context["vote_form"] = (
            modelformset_factory(
                AttendeeChoice,
                form=self.choice_form_class,
                extra=len(context["choices"]),
                fields=["status"],
                formset=ChoiceVoteBaseFormset,
            )
            if not vote_form
            else vote_form
        )
        return context

    def handle_no_permission(self):
        return redirect("unlock", uuid_slug=self.get_object().access_link)

    def test_func(self):
        """
        checks if the user is the user creator, has already entered the password
        or if the event is password protected.
        """
        obj = self.get_object()
        if (
            self.request.session.get(f"unlock-{obj.access_link}")
            or not obj.password_protect
            or (obj.user_id == self.request.user)
        ):
            return True
        else:
            return False

    def form_valid(self, request, attendee_form, vote_formset):
        # get db objects to save model forms
        choice_ids = request.POST.getlist("choice-id")
        choices = Choice.objects.filter(id__in=choice_ids)
        event = Event.objects.get(access_link=request.POST.get("event-uuid"))

        # save forms with foreign keys
        attendee = attendee_form.save(commit=False)
        attendee.event_id = event
        attendee.save()
        for i, formset in enumerate(vote_formset):
            vote = formset.save(commit=False)
            vote.choice_id = choices[i]
            vote.attendee_id = attendee
            vote.save()
        vote_formset.save()
        return redirect("home")

    def form_invalid(self, attendee_form, vote_form):
        return self.render_to_response(
            self.get_context_data(attendee_form=attendee_form, vote_form=vote_form)
        )

    def post(self, request, *args, **kwargs):
        attendee_form = self.attendee_form_class(request.POST)
        vote_formset_obj = modelformset_factory(
            AttendeeChoice,
            form=self.choice_form_class,
            extra=self.request.POST.get("total_rows"),
            fields=["status"],
            formset=ChoiceVoteBaseFormset,
        )
        vote_formset = vote_formset_obj(request.POST)

        if attendee_form.is_valid() and vote_formset.is_valid():
            return self.form_valid(request, attendee_form, vote_formset)
        else:
            return self.form_invalid(attendee_form, vote_formset)


class UnlockVoteView(UserPassesTestMixin, FormView):
    template_name = "unlock_vote.html"
    form_class = UnlockVoteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid_slug"] = self.kwargs.get("uuid_slug")
        context["event_data"] = Event.objects.get(access_link=context["uuid_slug"])
        return context

    def handle_no_permission(self):
        return redirect("vote", uuid_slug=self.kwargs["uuid_slug"])

    def test_func(self):
        obj = Event.objects.get(access_link=self.kwargs["uuid_slug"])
        # redirect to the vote page if test_func returns False
        if (
            self.request.session.get(f"unlock-{obj.access_link}")
            or not obj.password_protect
            or (obj.user_id == self.request.user)
        ):
            return False
        else:
            return True

    def form_valid(self, form):
        """
        password checking is implemented within the form"s clean_password
        method.
        """
        uuid_slug = form.data.get("event_id")
        self.request.session[f"unlock-{uuid_slug}"] = True
        return redirect("vote", uuid_slug=uuid_slug)


class ChoiceAddView(UserPassesTestMixin, TemplateView):
    template_name = "vote_add.html"
    form_class = ChoiceFormset

    def get_context_data(self, uuid_slug=None, form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        access_link = uuid_slug if uuid_slug else context.get("uuid_slug")
        context["event"] = Event.objects.get(access_link=access_link)
        context["choices_list"] = Choice.objects.filter(event_id=context["event"])
        context["forms"] = (
            form if form else self.form_class(queryset=Choice.objects.none())
        )
        return context

    def handle_no_permission(self):
        if Event.objects.get(access_link=self.kwargs["uuid_slug"]).allow_add:
            return super(self).handle_no_permission()
        else:
            raise PermissionDenied

    def test_func(self):
        obj = Event.objects.get(access_link=self.kwargs["uuid_slug"])
        if (
            (
                self.request.session.get(f"unlock-{obj.access_link}")
                or not obj.password_protect
            )
            and obj.allow_add
        ) or (obj.user_id == self.request.user):
            return True
        else:
            return False

    def form_valid(self, request, choice_formset):
        event = Event.objects.get(access_link=choice_formset.data.get("event"))
        for i, formset in enumerate(choice_formset):
            if formset.cleaned_data.get("DELETE"):
                continue
            choice = formset.save(commit=False)
            choice.event_id = event
            choice.save()
        return redirect("vote", uuid_slug=event.access_link)

    def form_invalid(self, request, choice_formset):
        return self.render_to_response(
            self.get_context_data(
                uuid_slug=choice_formset.data.get("event"), form=choice_formset
            )
        )

    def post(self, request, *args, **kwargs):
        choice_formset = self.form_class(request.POST)
        if choice_formset.is_valid():
            return self.form_valid(request, choice_formset)
        else:
            return self.form_invalid(request, choice_formset)


class ChoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "vote_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(access_link=context.get("uuid_slug"))
        context["choices"] = Choice.objects.filter(event_id=event)
        return context

    def test_func(self):
        obj = Event.objects.get(access_link=self.kwargs.get("uuid_slug"))
        return obj.user_id == self.request.user

    def post(self, request, *args, **kwargs):
        # Add support for browsers which only accept GET and POST similar to DeletionMixin.
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        del_ids = [key for key in request.POST.keys() if key.isnumeric()]
        del_objs = Choice.objects.filter(pk__in=del_ids)
        for obj in del_objs:
            obj.delete()
        return redirect("event", uuid_slug=self.kwargs.get("uuid_slug"))


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    model = Event

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.request.user.first_name
        return context


class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "event_detail.html"
    model = Event
    slug_url_kwarg = "uuid_slug"
    slug_field = "access_link"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choices"] = Choice.objects.filter(event_id=context.get("event"))
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    slug_url_kwarg = "uuid_slug"
    slug_field = "access_link"
    success_url = reverse_lazy("dashboard")
    template_name = "delete_event.html"

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user


class EventEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "edit_event.html"
    form_class = NewEventForm
    slug_url_kwarg = "uuid_slug"
    slug_field = "access_link"
    success_url = "/"

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user

from django.shortcuts import render
from datetime import date
from django.views import generic, View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormMixin
from django.shortcuts import redirect
from .forms import EventForm, EventRegistrationForm, ContactForm
from .models import Event, EventRegistration, ContactMessage


class UpcomingEventList(generic.ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        return (
            Event.objects
            .filter(status=1, date__gte=date.today())
            .order_by('date', 'time')
        )


class PastEventList(generic.ListView):
    model = Event
    template_name = 'events/past_events.html'
    context_object_name = 'past_events'
    paginate_by = 6

    def get_queryset(self):
        return (
            Event.objects
            .filter(status=1, date__lt=date.today())
            .order_by('-date', '-time')
        )


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_create.html'
    success_url = '/success?f=e'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'events/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['f'] = self.request.GET.get('f', 'a')
        return context


class EventDetails(FormMixin, DetailView):
    model = Event
    template_name = "events/event_details.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = EventRegistrationForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            try:
                registration = EventRegistration.objects.get(
                    event=event, user=user
                )
                form = EventRegistrationForm(instance=registration)
                context['already_registered'] = True
            except EventRegistration.DoesNotExist:
                form = EventRegistrationForm()
                context['already_registered'] = False
        else:
            form = EventRegistrationForm()

        context['form'] = form
        context['registrations'] = EventRegistration.objects.filter(
            event=event
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event = self.object

        # Handle cancellation
        if request.POST.get("cancel_registration"):
            EventRegistration.objects.filter(
                event=event, user=request.user
            ).delete()
            return redirect("event_details", slug=event.slug)

        # Handle update
        if request.POST.get("update_registration"):
            registration = EventRegistration.objects.get(
                event=event, user=request.user
            )
            new_note = request.POST.get("note")

            # Only update if the note has changed
            if new_note != registration.note:
                registration.note = new_note
                registration.save()
            return redirect("event_details", slug=event.slug)

        # Handle new registration
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            return redirect("event_details", slug=event.slug)

        registrations = EventRegistration.objects.filter(event=event)
        is_registered = EventRegistration.objects.filter(
            event=event, user=request.user
        ).exists()
        return render(
            request,
            "events/event_details.html",
            {
                "event": event,
                "form": form,
                "registrations": registrations,
                "is_registered": is_registered,
            },
        )


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'events/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return redirect('/success?f=c')
        return render(request, 'events/contact.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'events/about.html'

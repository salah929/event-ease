from django.shortcuts import render
from django.views import generic, View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormMixin
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from datetime import date
from .forms import EventCreateForm, EventRegistrationForm, ContactForm
from .forms import CustomLoginForm
from .models import Event, EventRegistration, ContactMessage


class UpcomingEventList(generic.ListView):
    """
    Displays a paginated list of upcoming published events,
    ordered by date and time.
    """
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        """
        Returns a queryset of upcoming published events,
        ordered by date and time.
        """
        return (
            Event.objects
            .filter(status=1, date__gte=date.today())
            .order_by('date', 'time')
        )


class PastEventList(generic.ListView):
    """
    Displays a paginated list of past published events,
    ordered by most recent first.
    """
    model = Event
    template_name = 'events/past_events.html'
    context_object_name = 'past_events'
    paginate_by = 6

    def get_queryset(self):
        """
        Returns a queryset of past published events,
        ordered by most recent date and time.
        """
        return (
            Event.objects
            .filter(status=1, date__lt=date.today())
            .order_by('-date', '-time')
        )


class EventCreateView(CreateView):
    """
    Handles the creation of a new event,
    assigning the logged-in user as the creator.
    """
    model = Event
    form_class = EventCreateForm
    template_name = 'events/event_create.html'
    success_url = '/success?f=e'

    def form_valid(self, form):
        """
        Sets the current user as the event creator before saving the form.
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SuccessView(TemplateView):
    """
    Renders a success page with context based on the 'f' GET parameter.
    """
    template_name = 'events/success.html'

    def get_context_data(self, **kwargs):
        """
        Adds the 'f' GET parameter to the context,
        defaulting to 'a' if not provided.
        """
        context = super().get_context_data(**kwargs)
        context['f'] = self.request.GET.get('f', 'a')
        return context


class EventDetails(FormMixin, DetailView):
    """
    Displays event details and manages event registrations.
    Handles displaying the registration form, viewing existing registrations,
    and processing registration, update, or cancellation
    by authenticated users.
    """
    model = Event
    template_name = "events/event_details.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = EventRegistrationForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        """
        Adds event registration form and registration status to the context.
        If the user is authenticated and already registered, pre-fills the form
        and sets a flag. Also includes all registrations for the event.
        """
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
        """
        Handles event registration form submissions.

        Supports:
        - New registration
        - Updating an existing registration note
        - Cancelling a registration

        Redirects back to the event detail page after each action.
        """
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
    """
    Handles displaying and processing the contact form.
    On valid submission, saves the message and redirects to a success page.
    """
    def get(self, request):
        form = ContactForm()
        return render(request, 'events/contact.html', {'form': form})

    def post(self, request):
        """
        Processes the submitted contact form.
        Saves the message if valid and redirects to the success page;
        otherwise, re-renders the form with validation errors.
        """
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
    """
    Renders the static About page of the events site.
    """
    template_name = 'events/about.html'


class CustomLoginView(LoginView):
    """
    Handles user login using a custom authentication form and template.
    """
    authentication_form = CustomLoginForm
    template_name = 'templates/account/login.html'

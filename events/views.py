from django.shortcuts import render
from datetime import date
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import EventForm
from .models import Event


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
    success_url = '/success'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'events/success.html'

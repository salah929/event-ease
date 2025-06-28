from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, date, time
from events.models import Event


class TestUpcomingEventListView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        today = date.today()

        self.approved_future_event = Event.objects.create(
            title="Future Event",
            description="An event in the future.",
            date=today + timedelta(days=1),
            time=time(10, 0),
            location="Berlin",
            status=1,
            created_by=self.user
        )

        self.approved_past_event = Event.objects.create(
            title="Past Event",
            description="An event in the past.",
            date=today - timedelta(days=1),
            time=time(14, 0),
            location="Berlin",
            status=1,
            created_by=self.user
        )

        self.pending_event = Event.objects.create(
            title="Pending Event",
            description="Should not be visible.",
            date=today + timedelta(days=2),
            time=time(9, 0),
            location="Berlin",
            status=0,
            created_by=self.user
        )

    def test_only_upcoming_approved_events_are_listed(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        events = response.context['events']
        self.assertIn(self.approved_future_event, events)
        self.assertNotIn(self.approved_past_event, events)
        self.assertNotIn(self.pending_event, events)

    def test_events_are_ordered_by_date_and_time(self):
        Event.objects.create(
            title="Earlier Future Event",
            description="Earlier than other future event.",
            date=self.approved_future_event.date,
            time=time(9, 0),
            location="Berlin",
            status=1,
            created_by=self.user
        )
        response = self.client.get(reverse('home'))
        events = list(response.context['events'])
        sorted_list = sorted(events, key=lambda e: (e.date, e.time))
        self.assertEqual(events, sorted_list)

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, date, time
from events.models import Event


class TestPastEventListView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        today = date.today()
        self.past_event = Event.objects.create(
            title="Past Event",
            description="An event in the past.",
            date=today - timedelta(days=1),
            time=time(14, 0),
            location="Berlin",
            status=1,
            created_by=self.user
        )

        self.future_event = Event.objects.create(
            title="Future Event",
            description="An event in the future.",
            date=today + timedelta(days=1),
            time=time(10, 0),
            location="Berlin",
            status=1,
            created_by=self.user
        )

        self.pending_past_event = Event.objects.create(
            title="Pending Past Event",
            description="Should not be visible.",
            date=today - timedelta(days=2),
            time=time(9, 0),
            location="Berlin",
            status=0,
            created_by=self.user
        )

    def test_only_past_approved_events_are_listed(self):
        response = self.client.get(reverse('past_events'))
        self.assertEqual(response.status_code, 200)

        events = response.context['past_events']
        self.assertIn(self.past_event, events)
        self.assertNotIn(self.future_event, events)
        self.assertNotIn(self.pending_past_event, events)

    def test_events_are_ordered_by_most_recent_first(self):
        Event.objects.create(
            title="More Recent Past Event",
            description="Happened yesterday morning.",
            date=self.past_event.date,
            time=time(15, 0),  # later than original past_event
            location="Berlin",
            status=1,
            created_by=self.user
        )
        response = self.client.get(reverse('past_events'))
        events = list(response.context['past_events'])
        sorted_events = sorted(
            events, key=lambda e: (e.date, e.time), reverse=True
            )
        self.assertEqual(events, sorted_events)

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, date, time
from events.models import Event


class TestEventCreateView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('event_create')

    def test_post_valid_event_creates_event(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Test Event',
            'description': 'Description.',
            'date': date.today() + timedelta(days=1),
            'time': time(10, 0),
            'location': 'Berlin'
        }
        self.client.post(self.url, data)
        self.assertEqual(Event.objects.count(), 1)

        event = Event.objects.first()
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.created_by, self.user)

    def test_missing_title(self):
        data = {
            'description': 'No title.',
            'date': date.today() + timedelta(days=1),
            'time': time(10, 0),
            'location': 'Berlin'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'title', 'This field is required.'
        )
        self.assertEqual(Event.objects.count(), 0)

    def test_missing_description(self):
        data = {
            'title': 'No Description',
            'date': date.today() + timedelta(days=1),
            'time': time(10, 0),
            'location': 'Berlin'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'description', 'This field is required.'
        )
        self.assertEqual(Event.objects.count(), 0)

    def test_missing_date(self):
        data = {
            'title': 'No Date',
            'description': 'Missing the date.',
            'time': time(10, 0),
            'location': 'Berlin'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'date', 'This field is required.'
        )
        self.assertEqual(Event.objects.count(), 0)

    def test_missing_time(self):
        data = {
            'title': 'No Time',
            'description': 'Missing the time.',
            'date': date.today() + timedelta(days=1),
            'location': 'Berlin'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'time', 'This field is required.'
        )
        self.assertEqual(Event.objects.count(), 0)

    def test_missing_location(self):
        data = {
            'title': 'No Location',
            'description': 'Missing the location.',
            'date': date.today() + timedelta(days=1),
            'time': time(10, 0)
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'location', 'This field is required.'
        )
        self.assertEqual(Event.objects.count(), 0)

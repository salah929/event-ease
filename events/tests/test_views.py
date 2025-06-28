from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, date, time
from events.models import Event, EventRegistration, ContactMessage
from events.forms import ContactForm


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


class TestEventDetailsView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Description',
            date=date.today() + timedelta(days=1),
            time=time(10, 0),
            location='Berlin',
            status=1,
            # slug='sample-event',
            created_by=self.user
        )
        self.url = reverse('event_details', kwargs={'slug': self.event.slug})

    def test_get_event_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertIn('form', response.context)

    def test_post_new_registration(self):
        self.client.login(username='testuser', password='testpass')
        data = {'note': 'I am in!'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.assertEqual(EventRegistration.objects.count(), 1)
        reg = EventRegistration.objects.first()
        self.assertEqual(reg.note, 'I am in!')
        self.assertEqual(reg.user, self.user)

    def test_post_update_registration(self):
        EventRegistration.objects.create(
            event=self.event, user=self.user, note='Old note'
        )
        self.client.login(username='testuser', password='testpass')
        data = {'note': 'Updated note', 'update_registration': '1'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        reg = EventRegistration.objects.get(event=self.event, user=self.user)
        self.assertEqual(reg.note, 'Updated note')

    def test_post_cancel_registration(self):
        EventRegistration.objects.create(event=self.event, user=self.user)
        self.client.login(username='testuser', password='testpass')
        data = {'cancel_registration': '1'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.assertFalse(EventRegistration.objects.filter(
            event=self.event, user=self.user
        ).exists())


class TestContactView(TestCase):

    def test_get_contact_page_renders_form(self):
        response = self.client.get(reverse('contactus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_post_valid_contact_form_creates_message(self):
        form_data = {
            'name': 'Mark Selby',
            'email': 'mark@example.com',
            'message': 'I would like to know more.'
        }
        self.client.post(reverse('contactus'), form_data)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Mark Selby')
        self.assertEqual(msg.email, 'mark@example.com')
        self.assertEqual(msg.message, 'I would like to know more.')

    def test_post_invalid_contact_form_shows_errors(self):
        form_data = {
            'name': '',
            'email': 'not-an-email',
            'message': ''
        }
        response = self.client.post(reverse('contactus'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/contact.html')
        self.assertFormError(
            response, 'form', 'name', 'This field is required.'
        )
        self.assertFormError(
            response, 'form', 'message', 'This field is required.'
        )
        self.assertEqual(ContactMessage.objects.count(), 0)

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, date, time
from events.models import Event, EventRegistration


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

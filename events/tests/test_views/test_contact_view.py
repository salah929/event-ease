from django.test import TestCase
from django.urls import reverse
from events.models import ContactMessage
from events.forms import ContactForm


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

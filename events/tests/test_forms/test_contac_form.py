from django.test import TestCase
from events.forms import ContactForm


class TestContactForm(TestCase):

    def test_form_valid_data(self):
        form_data = {
            'name': 'John Higgins',
            'email': 'john@example.com',
            'message': 'Hello, I would like more information.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_name(self):
        form_data = {
            'email': 'john@example.com',
            'message': 'Missing name field.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_missing_email(self):
        form_data = {
            'name': 'Mark Williams',
            'message': 'This email should be invalid.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalid_email(self):
        form_data = {
            'name': 'Mark Allen',
            'email': 'invalid-email',
            'message': 'This email should be invalid.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_missing_message(self):
        form_data = {
            'name': "Ronnie O'sullivan",
            'email': 'ronnie@example.com',
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

from django.test import TestCase
from events.forms import EventRegistrationForm


class TestEventRegistrationForm(TestCase):

    def test_form_valid_with_note(self):
        form_data = {
            'note': 'Looking forward to it!',
        }
        form = EventRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valid_without_note(self):
        form_data = {
            'note': '',
        }
        form = EventRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

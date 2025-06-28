from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from events.forms import EventCreateForm, EventRegistrationForm, ContactForm


class TestEventCreateForm(TestCase):

    def get_fake_image_file(self):
        """Returns a fake image file (not a real image, just mimics one)."""
        return SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61",  # minimal bytes for a GIF header
            content_type="image/jpeg"
        )

    def test_valid_data_submission(self):
        form_data = {
            'title': 'Sample Event',
            'description': 'This is a sample event.',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'Berlin',
        }
        image = self.get_fake_image_file()
        form = EventCreateForm(data=form_data, files={'featured_image': image})
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_accepts_missing_optional_image(self):
        form_data = {
            'title': 'No Image Event',
            'description': 'Event with no image provided.',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'Berlin',
        }
        form = EventCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_field_title(self):
        form_data = {
            'description': 'Missing title.',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'Berlin',
        }
        form = EventCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_missing_required_field_description(self):
        form_data = {
            'title': 'Missing description',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'Berlin',
        }
        form = EventCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_missing_required_field_date(self):
        form_data = {
            'title': 'Test Event',
            'description': 'Missing date',
            'time': timezone.now().time(),
            'location': 'Berlin',
        }
        form = EventCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_missing_required_field_time(self):
        form_data = {
            'title': 'Test Event',
            'description': 'Missing time',
            'date': timezone.now().date(),
            'location': 'Berlin',
        }
        form = EventCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_missing_required_field_location(self):
        form_data = {
            'title': 'Test Event',
            'description': 'Missing location',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
        }
        form = EventCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)


User = get_user_model()


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

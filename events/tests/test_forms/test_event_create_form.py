from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from events.forms import EventCreateForm


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

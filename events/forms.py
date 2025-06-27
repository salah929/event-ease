from django import forms
from .models import Event, EventRegistration, ContactMessage
from django.forms import ClearableFileInput
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'time',
            'location', 'featured_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time', 'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        one_week_later = datetime.now().date() + timedelta(weeks=1)
        self.fields['date'].initial = one_week_later
        self.fields['time'].initial = '09:00'

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        max_size_mb = 3

        if (
            image and
            hasattr(image, 'size') and
            image.size and
            image.size > max_size_mb * 1024 * 1024
        ):
            raise ValidationError(
                f"The image file is too large (>{max_size_mb}MB)."
            )
        return image


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['note']
        widgets = {
            'note': forms.TextInput(attrs={'class': 'form-control w-100'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5
            }),
        }

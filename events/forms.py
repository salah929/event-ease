from django import forms
from .models import Event, EventRegistration, ContactMessage


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']
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
        }


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

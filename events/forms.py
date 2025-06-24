from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5, 'id': "desc"
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time', 'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

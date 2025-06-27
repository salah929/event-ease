from django import forms
from django.forms import ClearableFileInput
from allauth.account.forms import LoginForm, SignupForm
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Event, EventRegistration, ContactMessage


class EventCreateForm(forms.ModelForm):
    """
    Form for creating an event with custom widgets,
    default values, and image size validation.
    """
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
        super(EventCreateForm, self).__init__(*args, **kwargs)
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
    """
    Form for registering to an event with an optional note input.
    """
    class Meta:
        model = EventRegistration
        fields = ['note']
        widgets = {
            'note': forms.TextInput(attrs={'class': 'form-control w-100'}),
        }


class ContactForm(forms.ModelForm):
    """
    Form for submitting a contact message with name, email, and message fields.
    """
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


class CustomLoginForm(LoginForm):
    """
    Customizes the login form with Bootstrap styling
    and placeholders for fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


class CustomSignupForm(SignupForm):
    """
    Extends the default signup form to include first and last name fields,
    with customized Bootstrap styling and placeholders.
    """
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Last Name'
        })
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the signup form with Bootstrap styling and placeholders
        for username, email, and password fields.
        """
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirm Password'
        })

    def save(self, request):
        """
        Saves the user and updates the first and last name from the form data
        before returning the user instance.
        """
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

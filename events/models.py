from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

STATUS = ((0, "Pending"), (1, "Approved"))


def generate_unique_slug(title, model):
    """
    Returns a unique slug for the given title
    by checking existing slugs in the model.
    If the slug already exists, appends a number to make it unique.
    """
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class Event(models.Model):
    """
    Represents an event with details such as title, date, location, and status.
    Automatically generates a unique slug on save if not provided.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to generate a unique slug
        from the title if not provided.
        """
        if not self.slug:
            self.slug = generate_unique_slug(self.title, Event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    """
    Links a user to an event registration with an optional note.
    Ensures a user can register only once per event.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name='registrations')
    note = models.CharField(max_length=255, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"


class ContactMessage(models.Model):
    """
    Stores messages submitted through a contact form,
    including sender info and timestamp.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

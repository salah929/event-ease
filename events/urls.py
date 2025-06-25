from django.urls import path
from . import views
from .views import EventCreateView, ContactView, AboutView

urlpatterns = [
    path('', views.UpcomingEventList.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contactus/', ContactView.as_view(), name='contactus'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('event/<slug:slug>/', views.EventDetails.as_view(),
         name='event_details'),
    path('past-events/', views.PastEventList.as_view(), name='past_events'),
    path('success/', views.SuccessView.as_view(), name='success'),
]

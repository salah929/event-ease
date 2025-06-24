from django.urls import path
from . import views
from .views import EventCreateView

urlpatterns = [
    path('', views.UpcomingEventList.as_view(), name='home'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('event/<slug:slug>/', views.EventDetails.as_view(),
         name='event_details'),
    path('past-events/', views.PastEventList.as_view(), name='past_events'),
    path('success/', views.SuccessView.as_view(), name='success'),
]

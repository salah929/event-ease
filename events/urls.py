from django.urls import path
from . import views

urlpatterns = [
    path('', views.UpcomingEventList.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contactus/', views.ContactView.as_view(), name='contactus'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<slug:slug>/', views.EventDetails.as_view(),
         name='event_details'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('past-events/', views.PastEventList.as_view(), name='past_events'),
    path('success/', views.SuccessView.as_view(), name='success'),
]

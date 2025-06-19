from django.urls import path
from . import views

urlpatterns = [
    path('', views.UpcomingEventList.as_view(), name='home'),
]

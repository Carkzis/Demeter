"""URL patterns for the users."""

from django.urls import path, include, reverse_lazy

from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    # Default authorisation urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    # Password reset urls.
]
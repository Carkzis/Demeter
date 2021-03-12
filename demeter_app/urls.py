"""Define url patterns."""

from django.urls import path

from . import views

app_name = 'demeter_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page for adding meals
    path('add_meal/', views.add_meal, name='add_meal'),
]
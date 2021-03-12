from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Nation(models.Model):
    """Contains a list of the countries."""
    country = models.CharField(max_length=50, primary_key=True)
    continent = models.CharField(max_length=20)
    national_dish = models.CharField(max_length=50)

    def __str__(self):
        return self.country

class Meal(models.Model):
    """Contains a list of meals and their details."""
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.CharField(max_length=50)
    country = models.ForeignKey(Nation, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.member} - Meal: {self.meal} - Country: {self.country} - \
Date Added: {self.date_added}'
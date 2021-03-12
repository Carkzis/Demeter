from django import forms

from .models import Meal, Nation

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['member', 'meal', 'country']
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.db.models import Count

from .forms import MealForm
from .models import Nation, Meal
from django.contrib.auth.decorators import login_required

def index(request):
    """The home page."""
    return render(request, 'demeter_app/index.html', {'continents': display_country_totals()})

@login_required
def add_meal(request):
    """Add meal."""
    if request.method != 'POST':
        form = MealForm()
    else:
        form = MealForm(data=request.POST)
        if form.is_valid:
            new_meal = form.save(commit=False)
            new_meal.member = request.user
            new_meal.save()
            return redirect('demeter_app:your_meals')

    context = {'form': form}
    return render(request, 'demeter_app/add_meal.html', context)

@login_required
def your_meals(request):
    """Displays all meals associated with a user."""
    meals = Meal.objects.all()
    context = {'meals': meals}
    return render(request, 'demeter_app/your_meals.html', context)

@login_required
def view_meal(request, meal_id):
    """Displays a single meal."""
    meal = Meal.objects.get(id=meal_id)
    context = {'meal': meal}
    return render(request, 'demeter_app/view_meal.html', context)

def display_country_totals():
    """Display the totals of countries."""
    continents = Nation.objects.values('continent').annotate(
        Count('continent')
    )
    continent_counts = {d['continent']: d['continent__count'] for d in continents}

    return continent_counts
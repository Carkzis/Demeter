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
    # Get the amount of different countries meals have been made for
    unique_countries = Meal.objects.order_by().values_list('country', flat=True).distinct()
    # Create k-v pairs of county and continent
    country_continents = Nation.objects.filter(country__in=unique_countries).values('country', 'continent')
    country_counter = {}
    # For loop to count countries completed
    # TODO: REFACTOR THIS!
    for country_continent in country_continents:
        key_entry = country_continent['continent']
        if key_entry not in country_counter:
            country_counter[key_entry] = 1
        else:
           country_counter[key_entry] += 1
    context = {
        'meals': meals,
        'countries': country_continents,
        'count': country_counter
        }
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
    # Create a k-v pair for continent and counts
    continent_counts = {d['continent']: d['continent__count'] for d in continents}

    return continent_counts
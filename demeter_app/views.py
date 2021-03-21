from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.http import Http404

from .forms import MealForm
from .models import Nation, Meal
from django.contrib.auth.decorators import login_required

import random

def index(request):
    """The home page."""
    continent_counts, total_countries = display_country_totals()
    context = {
        'countries_per': continent_counts,
        'total_countries': total_countries,
    }
    return render(request, 'demeter_app/index.html', context)

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
    meals = Meal.objects.filter(member=request.user).order_by('country')
    if not meals:
        meals = False
    country_continents, country_counter = completion_counter(request)
    context = {
        'meals': meals,
        'countries': country_continents,
        'count': country_counter
        }
    return render(request, 'demeter_app/your_meals.html', context)

@login_required
def stats(request):
    """Displays the stats regarding the completion of countries by continent."""
    country_continents, country_counter = completion_counter(request)
    country_totals, overall_total = display_country_totals()
    completion_percentages, overall_percent = completion_percent(country_counter, country_totals)
    next_continent = random_choice(
        request,
        completion_percentages,
        country_continents
        )
    context = {
        'countries': country_continents,
        'count': country_counter,
        'totals': country_totals,
        'percentages': completion_percentages,
        'overall_percent': overall_percent,
        'next': next_continent,
        }
    return render(request, 'demeter_app/stats.html', context)

def random_choice(request, completion_percentages, country_continents):
    """
    Suggests an new country to complete based on which continent
    you have done less of.
    """
    next_continent = min(
        completion_percentages,
        key=completion_percentages.get
        )

    # Gets a query set of all countries in next continent
    next_continent_options = Nation.objects.filter(
        continent=next_continent
        ).values_list('country', flat=True)
    meals_list = Meal.objects.filter(
        member=request.user
        ).values_list('country', flat=True)
    # Need to exclude any country already done from the selection
    next_continent_options = next_continent_options.exclude(country__in=meals_list)

    next_country = random.choice(next_continent_options)
    
    return next_country

def completion_counter(request):
    """Returns the countries where meals have been made."""
        # Get the amount of different countries meals have been made for
    unique_countries = Meal.objects.order_by().values_list(
        'country',
        flat=True
        ).distinct()
    unique_countries = unique_countries.filter(member=request.user)
    # Create k-v pairs of county and continent
    country_continents = Nation.objects.filter(
        country__in=unique_countries
        ).values('country', 'continent')
    country_counter = {}
    # For loop to count countries completed
    for country_continent in country_continents:
        key_entry = country_continent['continent']
        if key_entry not in country_counter:
            country_counter[key_entry] = 1
        else:
           country_counter[key_entry] += 1
    return country_continents, country_counter

def completion_percent(country_counter, country_totals):
    """Calculates percentage of continents completed, plus overall."""
    completion_percentages = {}
    overall_total = 0 # overall total of countries completed
    total_countries = 0 # Incase the amount of countries change!
    for k, v in country_totals.items():
        if k not in country_counter:
            country_counter[k] = 0
        completion_percentages[k] = str(round(
            (country_counter[k] / country_totals[k] * 100), 2
            )) + "%"
        overall_total += country_counter[k]
        total_countries += country_totals[k]
    # Add an overall percentage to the dictionary
    overall_percent = str(round(
           (overall_total / total_countries * 100), 2
           )) + "%"
    return completion_percentages, overall_percent

@login_required
def view_meal(request, meal_id):
    """Displays a single meal."""
    meal = Meal.objects.get(id=meal_id)
    # Redirect the member if they try to go to someone else's meal
    if meal.member != request.user:
        return redirect('demeter_app:your_meals')
    context = {'meal': meal}
    return render(request, 'demeter_app/view_meal.html', context)

def display_country_totals():
    """Display the totals of countries."""
    continents = Nation.objects.values('continent').annotate(
        Count('continent')
    )
    # Create a k-v pair for continent and counts
    continent_counts = {d['continent']: d['continent__count'] for d in continents}
    total_countries = 0
    for k, v in continent_counts.items():
        total_countries += v
    return continent_counts, total_countries
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import MealForm
from .models import Nation, Meal

def index(request):
    """The home page."""
    return render(request, 'demeter_app/index.html')

def import_page(request):
    """Import page."""
    return render(request, 'demeter_app/import.html')

class AddMeal(CreateView):
    model = Meal
    form_class = MealForm
    template_name = 'demeter_app/add_meal.html'

def add_meal(request):
    """Add meal."""
    if request.method != 'POST':
        form = MealForm()
    else:
        form = MealForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('demeter_app:index')

    context = {'form': form}
    return render(request, 'demeter_app/add_meal.html', context)


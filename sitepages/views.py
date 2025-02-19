from django.shortcuts import render
from django.views.generic import ListView
from .models import Drink

def landing_page(request):
    return render(request, 'site/landing.html')

class DrinkListView(ListView):
    model = Drink
    template_name = 'site/drink_list.html'
    context_object_name = 'drinks'
    ordering = ['category', 'name']

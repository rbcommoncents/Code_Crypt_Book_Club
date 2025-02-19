from django.urls import path 
from .views import landing_page, DrinkListView

urlpatterns = [
    path("", landing_page, name="landing"),
    path('drinks/', DrinkListView.as_view(), name='drink_list'),
]
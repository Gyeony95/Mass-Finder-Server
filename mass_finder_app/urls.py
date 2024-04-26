from django.urls import path, include
from .views import calc_mass

app_name = 'mass_finder_app'
urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
    path('api/calc_mass', calc_mass, name='calc_mass'),
]
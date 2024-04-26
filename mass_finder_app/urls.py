from django.urls import path, include

app_name = 'mass_finder_app'
urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]
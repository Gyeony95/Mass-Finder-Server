from django.shortcuts import render
from rest_framework import viewsets
from mass_finder_app.models import Test
from mass_finder_app.serializers import TestSerializers

# Create your views here.


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializers
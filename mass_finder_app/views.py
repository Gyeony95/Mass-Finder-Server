from django.shortcuts import render
from rest_framework import viewsets
from mass_finder_app.models import Test, AminoData
from mass_finder_app.serializers import TestSerializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializers


@csrf_exempt
def calc_mass(request):
    if request.method == 'POST':
        total_weight = request.POST.get('totalWeight')  # double
        init_amino = request.POST.get('initAmino')  # String
        current_formy_type = request.POST.get('currentFormyType')  # String
        current_ion_type = request.POST.get('currentIonType')  # String
        input_aminos = request.POST.get('inputAminos')  # Map<String, double>
        user = AminoData(
            total_weight=total_weight,
            init_amino=init_amino,
            current_formy_type=current_formy_type,
            current_ion_type=current_ion_type,
            input_aminos=input_aminos,
        )
        if user is not None:
            return JsonResponse({'email': user.email}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

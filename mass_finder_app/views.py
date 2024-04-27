from django.shortcuts import render
from rest_framework import viewsets
from mass_finder_app.models import Test, AminoData
from mass_finder_app.serializers import TestSerializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json


# Create your views here.


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializers


@csrf_exempt
def calc_mass(request):
    logging.basicConfig(level=logging.DEBUG)  # 모든 DEBUG 이상의 로그를 캡처
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # request.body는 bytes형태이므로 decode 필요
        total_weight = data.get('totalWeight')  # float
        init_amino = data.get('initAmino')  # string
        current_formy_type = data.get('currentFormyType')  # string
        current_ion_type = data.get('currentIonType')  # string
        input_aminos = data.get('inputAminos')  # dict
        logging.debug(
            f"total_weight : {total_weight}, init_amino : {init_amino}, current_formy_type : {current_formy_type}, current_ion_type : {current_ion_type}, input_aminos : {input_aminos}")
        # if user is not None:
        #     return JsonResponse({'email': user.email}, status=200)
        # else:
        #     return JsonResponse({'error': 'Invalid credentials'}, status=400)
    # return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'success': 'calc compleate : '}, status=200)

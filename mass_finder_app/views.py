from django.shortcuts import render
from rest_framework import viewsets

from mass_finder_app.logic.amino_calc import calc, calc_by_ion_type
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
    if request.method != 'POST':
        return JsonResponse({"resultCode": 405, "resultMessage": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        logging.debug("Received data: %s", data)
        total_weight = data.get('totalWeight')  # float
        init_amino = data.get('initAmino')  # string
        current_formy_type = data.get('currentFormyType')  # string
        current_ion_type = data.get('currentIonType')  # string
        input_aminos = data.get('inputAminos')  # dict

        result = calc_by_ion_type(total_weight, init_amino, current_formy_type, current_ion_type, input_aminos)
        response = {
            "resultCode": 200,
            "resultMessage": "정상적으로 처리되었습니다.",
            "data": result,
        }
        return JsonResponse(response, status=200)

    except json.JSONDecodeError as e:
        logging.error("JSON decode error: %s", e)
        return JsonResponse({"resultCode": 400, "resultMessage": "Bad Request: Invalid JSON"}, status=400)
    except KeyError as e:
        logging.error("Missing key in data: %s", e)
        return JsonResponse({"resultCode": 400, "resultMessage": "Bad Request: Missing data"}, status=400)
    except Exception as e:
        logging.error("Error processing data: %s", e)
        return JsonResponse({"resultCode": 500, "resultMessage": "Internal Server Error"}, status=500)


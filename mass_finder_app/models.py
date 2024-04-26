from django.db import models


# Create your models here.

class Test(models.Model):
    test = models.CharField(max_length=10)

    def __str__(self):
        return self.test


# api input 에 사용되는 모델
class AminoData(models.Model):
    total_weight = models.FloatField()  # double 타입
    init_amino = models.CharField(max_length=100)  # 문자열 타입
    current_formy_type = models.CharField(max_length=100)  # 문자열 타입
    current_ion_type = models.CharField(max_length=100)  # 문자열 타입
    input_aminos = models.JSONField()  # Map<String, double> JSON 타입

    def __str__(self):
        return f'{self.init_amino} - {self.current_formy_type}'

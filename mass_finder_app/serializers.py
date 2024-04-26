from rest_framework import serializers
from mass_finder_app.models import Test


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = 'test'

from rest_framework import serializers
from .models import PickupLocation

class PickupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupLocation
        fields = '__all__'

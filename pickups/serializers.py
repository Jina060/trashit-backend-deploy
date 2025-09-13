from rest_framework import serializers
from .models import PickupRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class PickupRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    plan_id = serializers.PrimaryKeyRelatedField(source='plan', queryset=PickupRequest._meta.get_field('plan').related_model.objects.all(), write_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location', queryset=PickupRequest._meta.get_field('location').related_model.objects.all(), write_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(source='payment', queryset=PickupRequest._meta.get_field('payment').related_model.objects.all(), write_only=True)

    class Meta:
        model = PickupRequest
        fields = [
            'id',
            'user',
            'plan_id',
            'location_id',
            'pickup_datetime',
            'payment_id',
            'assignment',
            'created_at',
        ]
        read_only_fields = ['assignment', 'created_at']

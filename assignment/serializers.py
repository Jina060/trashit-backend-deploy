from rest_framework import serializers
from .models import CollectorAssignment
from .models import TrashCollectorProfile
from accounts.serializers import CustomUserSerializer 

class CollectorAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorAssignment
        fields = '__all__'

class TrashCollectorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True) # Nested user info

    class Meta:
        model = TrashCollectorProfile
        fields = '__all__'
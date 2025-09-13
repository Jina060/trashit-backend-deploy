from rest_framework.viewsets import ModelViewSet
from .models import PickupRequest
from .serializers import PickupRequestSerializer

class PickupRequestViewSet(ModelViewSet):
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer

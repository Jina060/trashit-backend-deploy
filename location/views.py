from rest_framework.viewsets import ModelViewSet
from .models import PickupLocation
from .serializers import PickupLocationSerializer

class PickupLocationViewSet(ModelViewSet):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer

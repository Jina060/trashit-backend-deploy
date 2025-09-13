from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CollectorAssignment, TrashCollectorProfile
from .serializers import TrashCollectorProfileSerializer, CollectorAssignmentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from location.models import PickupLocation
from math import radians, cos, sin, asin, sqrt, atan2
from rest_framework import status
import math
from rest_framework.permissions import AllowAny

class CollectorAssignmentViewSet(ModelViewSet):
    queryset = CollectorAssignment.objects.all()
    serializer_class = CollectorAssignmentSerializer

class TrashCollectorProfileViewSet(ModelViewSet):
    queryset = TrashCollectorProfile.objects.select_related('user').all()
    serializer_class = TrashCollectorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return collector profiles
        return super().get_queryset().filter(user__role='collector')

    def perform_create(self, serializer):
        # want collectors to create their own profiles
        serializer.save(user=self.request.user)
 
def haversine_distance(lat1, lon1, lat2, lon2):
    # Ensure all inputs are float 
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius = 6371  # Radius of Earth in kilometers
    return radius * c

@api_view(['GET'])
@permission_classes([AllowAny])
def suggest_collectors(request):
    try:
        lat = float(request.query_params.get('lat'))
        lng = float(request.query_params.get('lng'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid or missing lat/lng parameters.'},
                        status=status.HTTP_400_BAD_REQUEST)

    collectors = TrashCollectorProfile.objects.filter(is_available=True, latitude__isnull=False, longitude__isnull=False)

    collectors_with_distance = []
    for collector in collectors:
        distance = haversine_distance(lat, lng, collector.latitude, collector.longitude)
        collectors_with_distance.append((collector, distance))

    # Sort by distance and get top 2
    top_collectors = sorted(collectors_with_distance, key=lambda x: x[1])[:2]

    data = []
    for collector, distance in top_collectors:
        data.append({
            'id': collector.id,
            'name': collector.user.get_full_name(),
            'username': collector.user.username,
            'phone_number': collector.phone_number,
            'latitude': float(collector.latitude),
            'longitude': float(collector.longitude),
            'distance_km': round(distance, 2),
        })

    return Response({'suggested_collectors': data})


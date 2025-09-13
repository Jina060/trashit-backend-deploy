# pickup/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PickupRequestViewSet

router = DefaultRouter()
router.register(r'requests', PickupRequestViewSet, basename='pickup-request')

urlpatterns = [
    path('', include(router.urls)),
]

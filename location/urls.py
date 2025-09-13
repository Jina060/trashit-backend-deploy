from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PickupLocationViewSet

router = DefaultRouter()
router.register(r'locations', PickupLocationViewSet, basename='pickup-location')

urlpatterns = router.urls

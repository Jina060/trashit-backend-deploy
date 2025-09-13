from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectorAssignmentViewSet, TrashCollectorProfileViewSet
from .views import suggest_collectors

router = DefaultRouter()
router.register(r'assignments', CollectorAssignmentViewSet, basename='collector-assignment')
router.register(r'trash-Collectors', TrashCollectorProfileViewSet, basename='trash-collector-profile')

urlpatterns = [
    path("", include(router.urls)),
    path("suggest/", suggest_collectors),
]
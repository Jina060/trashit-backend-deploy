from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PaymentTransactionViewSet

router = DefaultRouter()
router.register(r'transactions', PaymentTransactionViewSet, basename='payment-transaction')

urlpatterns = router.urls

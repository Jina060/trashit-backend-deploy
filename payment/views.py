from rest_framework.viewsets import ModelViewSet
from .models import PaymentTransaction
from .serializers import PaymentTransactionSerializer

class PaymentTransactionViewSet(ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer

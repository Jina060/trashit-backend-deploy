from django.db import models
from django.contrib.auth import get_user_model
from subscription.models import SubscriptionPlan
from location.models import PickupLocation
from payment.models import PaymentTransaction
from assignment.models import CollectorAssignment
from django.utils import timezone 

User = get_user_model()

class PickupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(PickupLocation, on_delete=models.CASCADE, null=True, blank=True)
    pickup_datetime = models.DateTimeField(default=timezone.now)
    payment = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, null=True, blank=True)
    assignment = models.ForeignKey(CollectorAssignment, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"

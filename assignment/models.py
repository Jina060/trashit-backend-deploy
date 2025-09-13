from django.db import models
from accounts.models import CustomUser

class CollectorAssignment(models.Model):
    collector = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'collector'})
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collector: {self.collector.username}"

class TrashCollectorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'collector'})
    phone_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.collector.username}'s Profile"
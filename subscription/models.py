from django.db import models

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('on_demand', 'On Demand'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.get_name_display()

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('collector', 'Trash Collector'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'full_name', 'role']

    def __str__(self):
        return self.email



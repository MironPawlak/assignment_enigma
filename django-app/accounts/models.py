from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CUSTOMER = 'CR'
    SELLER = 'SR'
    USER_ROLES = [
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
    ]
    role = models.CharField(max_length=64, choices=USER_ROLES, blank=True, null=True)

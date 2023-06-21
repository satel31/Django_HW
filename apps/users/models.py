from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Email', unique=True)

    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Phone number', **NULLABLE)
    country = models.CharField(max_length=235, verbose_name='Country', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

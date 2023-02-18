from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user, get_user_model

class Jobs(models.Model):
    title = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    agent = models.CharField(max_length=255)
    data_added = models.DateTimeField(auto_now_add=True)
    create_user_company = models.CharField(max_length=255)

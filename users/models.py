from django.db import models   # Noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

from core.models import BaseModel

# Create your models here.


class BaseUser(BaseModel, AbstractBaseUser):
    class Meta:
        abstract = True


class User(BaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[])

    USERNAME_FIELD = 'email'

    objects = BaseUserManager

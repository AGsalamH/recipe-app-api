from django.db import models   # Noqa
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

from core.models import BaseModel
from django.core.validators import validate_email
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        validate_email(email)
        user = self.model(email = email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self._create_user(email, password, **extra_fields)


class BaseUser(BaseModel, AbstractBaseUser):
    class Meta:
        abstract = True


class User(BaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )



    USERNAME_FIELD = 'email'

    objects = UserManager()

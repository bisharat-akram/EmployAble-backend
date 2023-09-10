from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import user_type_choices, user_auth_choices
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

# Create your models here.

class User(AbstractUser):
    """ Class to store every user related detail """
    user_type = models.IntegerField(choices=user_type_choices, blank=True, null=True)
    auth_type = models.IntegerField(choices=user_auth_choices, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

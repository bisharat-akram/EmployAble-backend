from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import user_type_choices, user_auth_choices, education_level_choices, degree_type
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from .validators import phone_validator

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

    def __str__(self):
        """ method to return string representation """
        return f"{self.id} | {self.first_name}, {self.last_name} | {self.email} | {self.user_type}"

class Jobs(models.Model):
    """ model to store list of jobs """
    name = models.CharField(max_length = 50)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        """ method to return string representation """
        return self.name

class Skills(models.Model):
    """ model to store list of skills """
    name = models.CharField(max_length = 50)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        """ method to return string representation """
        return self.name

class UserProfile(models.Model):
    """ Model to store profile details of a user """
    user = models.OneToOneField(User, related_name="user_profile", related_query_name="user_profile", on_delete=models.CASCADE)
    field_name = models.TextField(null=True)
    description = models.TextField(max_length = 1000, null=True)
    phone_number = models.CharField(max_length = 16, validators = [phone_validator], unique = True, null=True)
    interested_jobs = models.ManyToManyField(Jobs)
    skills = models.ManyToManyField(Skills)
    prior_highest_education = models.IntegerField(choices = education_level_choices, null=True)

    def __str__(self):
        """ method to return string representation """
        return f"{self.id} | {self.phone_number} | {self.user.email}"

class Employment(models.Model):
    """ Class to store employment details for clients """
    employer_name = models.CharField(max_length = 50)
    position = models.CharField(max_length = 50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    user_profile = models.ForeignKey(UserProfile, related_name="employment_history", related_query_name="employment_history", on_delete=models.CASCADE)

class Education(models.Model):
    """ Class to store education details for clients """
    degree_type = models.IntegerField(choices=degree_type)
    major = models.CharField(max_length=50)
    university_name = models.CharField(max_length=50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    user_profile = models.ForeignKey(UserProfile, related_name="education_history", related_query_name="education_history", on_delete=models.CASCADE)
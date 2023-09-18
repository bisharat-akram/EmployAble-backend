from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Employment, Education, Jobs, Skills
# Register your models here.

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    """ Class to render job view in admin panel """
    list_display = ["name",]

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    """ Class to render job view in admin panel """
    list_display = ["name",]

class EmploymentInline(admin.StackedInline):
    """ class to render employment at user profile page in admin panel """
    model = Employment
    extra = 1

class EducationInline(admin.StackedInline):
    """ class to render education at user profile page in admin panel """
    model = Education
    extra = 1

@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'user_type', 'auth_type']
    fieldsets = (
        ('User Info', {'fields': ('username', 'password')}),
        ('Information Personal', {'fields': (
            'first_name',
            'last_name',
            'email',
            'user_type',
            'auth_type'
        )}),
        ('Permissiosn', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """ class to render user profile admin view at admin panel """
    list_display = ["id", "user", "phone_number"]
    inlines= [EducationInline, EmploymentInline]
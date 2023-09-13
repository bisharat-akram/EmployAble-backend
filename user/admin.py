from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

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
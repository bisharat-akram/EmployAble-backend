from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """ class to serialize user object """

    class Meta:
        model = User
        fields = ["id", "last_login", "username", "date_joined", "user_type", "auth_type", "first_name", "last_name", "email"]
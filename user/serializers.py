from rest_framework import serializers
from .models import User, Jobs, Skills, UserProfile, Employment, Education

class UserSerializer(serializers.ModelSerializer):
    """ class to serialize user object """
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "date_joined", "user_type", "auth_type", "first_name", "last_name", "email"]

class JobsSerializer(serializers.ModelSerializer):
    """ serializer to serialize job """
    class Meta:
        model = Jobs
        fields = "__all__"

class SkillsSerializer(serializers.ModelSerializer):
    """ serializer to serialize job """
    class Meta:
        model = Skills
        fields = "__all__"

class EmploymentSerializer(serializers.ModelSerializer):
    """ serializer to serialize employment model object """

    class Meta:
        model = Employment
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    """ serializer to serialize education model object """

    class Meta:
        model = Education
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer to serializer user profile data """
    user = UserSerializer()
    interested_jobs = JobsSerializer(many = True)
    skills = SkillsSerializer(many = True)
    employment_history = serializers.SerializerMethodField()
    education_history = serializers.SerializerMethodField()

    def get_employment_history(self, obj):
        """ method to get employment history for a user profile """
        return EmploymentSerializer(obj.employment_history, many = True).data
    
    def get_education_history(self, obj):
        """ method to get employment history for a user profile """
        return EducationSerializer(obj.education_history, many = True).data

    class Meta:
        model = UserProfile
        fields = "__all__"
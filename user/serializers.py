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

    def create(self, validated_data):
        validated_data["user_profile"] = self.context['request'].user.user_profile
        return super().create(validated_data)
    class Meta:
        model = Employment
        fields = "__all__"
        read_only_fields = ("user_profile", )


class EducationSerializer(serializers.ModelSerializer):
    """ serializer to serialize education model object """
    # degree_type_value = serializers.SerializerMethodField()

    # def get_field_names(self, declared_fields, info):
    #     expanded_fields = super(serializers.ModelSerializer, self).get_field_names(declared_fields, info)

    #     if getattr(self.Meta, 'extra_fields', None):
    #         return expanded_fields + self.Meta.extra_fields
    #     else:
    #         return expanded_fields

    # def get_degree_type_value(self, obj):
    #     """ method to get degree type display value """
    #     return obj.get_degree_type_display()

    def create(self, validated_data):
        validated_data["user_profile"] = self.context['request'].user.user_profile
        return super().create(validated_data)
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ("user_profile", )
        # extra_fields = ("degree_type_value",)

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer to serializer user profile data """
    user = UserSerializer()
    interested_jobs = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    employment_history = serializers.SerializerMethodField()
    education_history = serializers.SerializerMethodField()

    def get_interested_jobs(self, obj):
        """ method to get jobs ids """
        return list(obj.interested_jobs.all().values_list("id", flat=True))

    def get_skills(self, obj):
        """ method to get skills ids """
        return list(obj.skills.all().values_list("id", flat=True))

    def get_employment_history(self, obj):
        """ method to get employment history for a user profile """
        return EmploymentSerializer(obj.employment_history, many = True).data
    
    def get_education_history(self, obj):
        """ method to get employment history for a user profile """
        return EducationSerializer(obj.education_history, many = True).data

    class Meta:
        model = UserProfile
        fields = "__all__"

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """ Serializer to serializer user profile data """
    user = UserSerializer()
    interested_jobs = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    employment_history = serializers.SerializerMethodField()
    education_history = serializers.SerializerMethodField()
    prior_highest_education = serializers.SerializerMethodField()
    criminal_conviction = serializers.SerializerMethodField()

    def get_prior_highest_education(self, obj):
        """ method to get prior highest education name """
        return obj.get_prior_highest_education_display()
    
    def get_criminal_conviction(self, obj):
        """ method to get prior criminal conviction name """
        return obj.get_criminal_conviction_display()

    def get_interested_jobs(self, obj):
        """ method to get jobs ids """
        return JobsSerializer(obj.interested_jobs.all(), many = True).data

    def get_skills(self, obj):
        """ method to get skills ids """
        return SkillsSerializer(obj.skills.all(), many = True).data

    def get_employment_history(self, obj):
        """ method to get employment history for a user profile """
        return EmploymentSerializer(obj.employment_history, many = True).data
    
    def get_education_history(self, obj):
        """ method to get employment history for a user profile """
        return EducationSerializer(obj.education_history, many = True).data

    class Meta:
        model = UserProfile
        fields = "__all__"
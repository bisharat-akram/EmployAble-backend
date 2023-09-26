from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import *
from .models import User
import requests
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserSignUPView(APIView):
    """ View to login a user """
    permission_classes = (AllowAny,)

    def post(self, request):
        """ function to login """
        if User.objects.filter(email = request.data['email']).exists():
            raise ValidationError("User already exists with this email")
        try:
            user_obj = User(
                email = request.data['email'],
                first_name = request.data['first_name'],
                last_name = request.data['last_name'],
                user_type = request.data['user_type'],
                username = request.data['email'],
            )
            user_obj.set_password(request.data['password'])
            user_obj.save()
            if user_obj.user_type == 1: # create user profile object if user is client type
                UserProfile.objects.create(user = user_obj)
            user_data = UserSerializer(user_obj).data
            refresh_token = RefreshToken.for_user(user_obj)
            user_data['access'] = str(refresh_token.access_token)
            user_data['refresh'] = str(refresh_token)
            return Response(user_data)
        except Exception as e:
            raise ValidationError(e)
        

class GetUserView(APIView):
    """ View to get user data """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ method to get user data """
        return Response(UserSerializer(request.user).data)
    

class GoogleLoginView(APIView):
    """ View to create google login accounts in database """
    permission_classes = (AllowAny,)

    def post(self, request):
        """ Method to create google users in database """
        try:
            google_access_token = request.data['access_token']
            google_user_info_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,birthdays"
            headers = {'Authorization': f'Bearer {google_access_token}'}
            response = requests.get(google_user_info_url, headers = headers)
            if response.status_code == 200:
                response = response.json()
                email = response['emailAddresses'][0]['value']
                if User.objects.filter(email = email).exists():
                    user_obj = User.objects.get(email = email)
                    refresh_token = RefreshToken.for_user(user_obj)
                    return Response({
                        "access": str(refresh_token.access_token),
                        "refresh": str(refresh_token)
                    })
                else:
                    user_obj = User(
                        email = response['emailAddresses'][0]['value'],
                        first_name = response['names'][0]['givenName'],
                        last_name = response['names'][0]['familyName'],
                        password = "createdByGoogleAccount",
                        user_type = 1,
                        username = response['emailAddresses'][0]['value'],
                        auth_type = 1
                    )
                    user_obj.save()
                    UserProfile.objects.create(user = user_obj)
                    refresh_token = RefreshToken.for_user(user_obj)
                    return Response({
                        "access": str(refresh_token.access_token),
                        "refresh": str(refresh_token)
                    })
            else:
                raise ValidationError(response.json())
        except Exception as e:
            raise ValidationError(e)


class GetJobsView(ListAPIView):
    """ View to get list of jobs """

    permission_classes = (AllowAny,)
    serializer_class = JobsSerializer
    queryset = Jobs.objects.all()

class GetSkillsView(ListAPIView):
    """ View to get list of jobs """
    
    permission_classes = (AllowAny,)
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()

class GetProfileView(RetrieveAPIView, UpdateAPIView):
    """ View to get user profile """

    permission_classes = (IsAuthenticated, )
    serializer_class = UserProfileSerializer
    lookup_field = None

    def get_object(self):
        return self.request.user.user_profile
    
    def update(self, request, *args, **kwargs):
        """ Method to update the user profile """
        try:
            user_data = request.data.get('user')
            if user_data:
                request.data.pop('user')
                User.objects.filter(id = request.user.id).update(**user_data)

            interested_jobs = request.data.get('interested_jobs')
            skills = request.data.get('skills')

            if interested_jobs:
                request.data.pop('interested_jobs')
                request.user.user_profile.interested_jobs.set(interested_jobs)

            if skills:
                request.data.pop('skills')
                request.user.user_profile.skills.set(skills)

            if len(request.data.keys()) > 0:
                UserProfile.objects.filter(id = self.request.user.user_profile.id).update(**request.data)
            return Response(UserProfileSerializer(UserProfile.objects.filter(id = self.request.user.user_profile.id).first()).data)
        except Exception as e:
            raise ValidationError(e)
    
class EmploymentView(DestroyAPIView, CreateAPIView):
    """ view to delete / add employment history """
    permission_classes = (IsAuthenticated, )
    serializer_class = EmploymentSerializer
    
    def get_queryset(self):
        return Employment.objects.filter(user_profile__user__id = self.request.user.id)
    
class EducationView(DestroyAPIView, CreateAPIView):
    """ view to delete / add education history """
    permission_classes = (IsAuthenticated, )
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user_profile__user__id = self.request.user.id)
    

class GetProfileListView(APIView):
    """ Class to get list of user profiles """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ method to user profiles """
        queryset = {}

        if request.GET.get('skills'):
            queryset['skills__in'] = request.GET.get('skills').split(",")

        if request.GET.get('interested_jobs'):
            queryset['interested_jobs__in'] = request.GET.get('interested_jobs').split(",")
        
        if request.GET.get('prior_highest_education'):
            queryset['prior_highest_education'] = request.GET.get('prior_highest_education')

        if request.GET.get('search'):
            queryset['description__icontains'] = request.GET.get('search')

        serialized_user_profiles = UserProfileSerializer(UserProfile.objects.filter(**queryset), many = True)
        return Response(serialized_user_profiles.data)
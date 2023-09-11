from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer
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
            return Response(UserSerializer(user_obj).data)
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
        google_access_token = request.data['access_token']
        google_user_info_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,birthdays"
        headers = {'Authorization': f'Bearer {google_access_token}'}
        try:
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
                    refresh_token = RefreshToken.for_user(user_obj)
                    return Response({
                        "access": str(refresh_token.access_token),
                        "refresh": str(refresh_token)
                    })
            else:
                raise ValidationError(response.json())
        except Exception as e:
            raise ValidationError(e)



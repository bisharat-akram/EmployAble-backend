from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer
from .models import User
import pdb


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

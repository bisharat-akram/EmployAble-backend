from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', UserSignUPView.as_view(), name="signup_for_a_user"),
    path('google-login/', GoogleLoginView.as_view(), name="signup_for_a_user"),
    path('login/', TokenObtainPairView.as_view(), name="get_token_with_email_password"),
    path('me', GetUserView.as_view(), name="get_current_user_data"),
]
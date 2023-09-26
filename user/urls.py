from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', UserSignUPView.as_view(), name="signup_for_a_user"),
    path('google-login/', GoogleLoginView.as_view(), name="signup_for_a_user"),
    path('login/', TokenObtainPairView.as_view(), name="get_token_with_email_password"),
    path('me', GetUserView.as_view(), name="get_current_user_data"),
    path('jobs', GetJobsView.as_view(), name="get_jobs_list"),
    path('skills', GetSkillsView.as_view(), name="get_skills_list"),
    path('profile', GetProfileView.as_view(), name="get_profile_view"),
    path('profiles', GetProfileListView.as_view(), name="get_profile_view"),
    path('employment/<int:pk>', EmploymentView.as_view(), name="add/delete_employment"),
    path('employment/', EmploymentView.as_view(), name="add/delete_employment"),
    path('education/<int:pk>', EducationView.as_view(), name="add/delete_education"),
    path('education/', EducationView.as_view(), name="add/delete_education")
]
from users.apps import UsersConfig

from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import UserLoginView, UserRegister, email_verification, UserProfile, UserProfileUpdate

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegister.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),

    path('profile/', UserProfile.as_view(), name='profile'),
    path('change-profile/', UserProfileUpdate.as_view(), name='profile_update'),
]

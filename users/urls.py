from users.apps import UsersConfig

from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import UserLoginView, UserRegister

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegister.as_view(), name='register'),
]

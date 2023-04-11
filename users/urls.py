from django.shortcuts import redirect
from django.urls import path

from users.views import LoginView, LogoutView, RegisterUserAPIView

urlpatterns = [
    path("", lambda request: redirect("login")),
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserRegisterView, UserViewSet

router = DefaultRouter()

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserViewSet.as_view({"post": "login"}), name="user-login"),
    path(
        "delete-user/",
        UserViewSet.as_view({"post": "delete_user"}),
        name="user-delete-user",
    ),
    path(
        "forget-password/",
        UserViewSet.as_view({"post": "forget_password"}),
        name="user-forget-password",
    ),
    path(
        "reset-password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="user-reset-password",
    ),
    path(
        "change-password/",
        UserViewSet.as_view({"post": "change_password"}),
        name="user-change-password",
    ),
    path(
        "change-email/",
        UserViewSet.as_view({"post": "change_email"}),
        name="user-change-email",
    ),
    path(
        "change-username/",
        UserViewSet.as_view({"post": "change_username"}),
        name="user-change-username",
    ),
    path("logout/", UserViewSet.as_view({"post": "logout"}), name="user-logout"),
    path("me/", UserViewSet.as_view({"get": "me"}), name="user-me"),
]

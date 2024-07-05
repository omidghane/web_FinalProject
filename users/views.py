from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .auth import Auth
from .models import CustomUser
from .serializers import CustomUserSerializer, UserRegisterSerializer


class UserRegisterView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "post"]

    @action(
        detail=False,
        methods=["post"],
        url_path="user-logout",
        url_name="user-logout",
        permission_classes=[],
        authentication_classes=[],
    )
    def logout(self, request: Request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[Auth],
    )
    def delete_user(self, request: Request):
        try:
            user = request.user
            if not user or user.is_deleted:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.is_deleted = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], premission_classes=[])
    def forget_password(self, request: Request):
        try:
            user = CustomUser.objects.get(email=request.data["email"])
            user.send_reset_password_email()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[Auth],
        permission_classes=[IsAuthenticated],
    )
    def reset_password(self, request: Request):
        try:
            user = request.user
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[Auth],
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request: Request):
        try:
            user = request.user
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[Auth],
        permission_classes=[IsAuthenticated],
    )
    def change_email(self, request: Request):
        try:
            user = request.user
            user.email = request.data["email"]
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[Auth],
        permission_classes=[IsAuthenticated],
    )
    def change_username(self, request: Request):
        try:
            user = request.user
            user.username = request.data["username"]
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        authentication_classes=[Auth],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request):
        user = request.user
        if user:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

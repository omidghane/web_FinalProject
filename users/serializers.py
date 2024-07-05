from typing import Any

from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    is_banned = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "is_staff",
            "is_banned",
            "is_verified",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "username"]

    def create(self, validated_data: Any) -> CustomUser:
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

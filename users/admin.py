from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "username")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Status", {"fields": ("is_banned", "is_verified", "is_deleted")}),
        (
            "Social Media",
            {
                "fields": (
                    "has_telegram",
                    "has_instagram",
                    "has_facebook",
                    "has_website",
                    "has_whatapp",
                    "has_twitter",
                    "has_linkedin",
                    "has_rubika",
                    "has_bale",
                    "has_aparat",
                    "has_youtube",
                    "has_tiktok",
                    "has_snapchat",
                    "has_pinterest",
                    "has_github",
                    "has_gitlab",
                    "has_bitbucket",
                    "has_stackoverflow",
                    "has_medium",
                    "has_devto",
                    "has_reddit",
                    "has_twitch",
                    "has_discord",
                    "has_slack",
                    "has_trello",
                    "has_jira",
                    "has_asana",
                    "has_google",
                    "has_microsoft",
                    "has_amazon",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_banned",
        "is_verified",
        "is_deleted",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined", "email")

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_banned",
        "is_verified",
        "is_deleted",
    )


admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin

from .models import CustomUser

# class CutomUserAdmin(inline)

admin.site.register(CustomUser)

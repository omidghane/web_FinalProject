from django.contrib import admin

from .models import SubTask, Task

admin.site.register(Task)
admin.site.register(SubTask)

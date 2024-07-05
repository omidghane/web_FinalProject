import uuid

from django.db import models

from django.contrib.auth import get_user_model
from workspaces.models import Workspace

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [(1, "Planned"), (2, "In Progress"), (3, "Completed")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    estimated_time = models.IntegerField(blank=True, null=True)
    actual_time = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=50)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)


class SubTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

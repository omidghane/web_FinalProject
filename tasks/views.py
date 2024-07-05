from math import log

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.auth import Auth
from workspaces.models import UserWorkspaceRole, Workspace

from .models import SubTask, Task
from .serializer import SubTaskSerailizer, TaskSerailizer

User = get_user_model()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerailizer
    authentication_classes = [Auth]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_workspace_roles = UserWorkspaceRole.objects.filter(user=user)
        workspace_ids = user_workspace_roles.values_list("workspace_id", flat=True)
        return Task.objects.filter(workspace_id__in=workspace_ids)

    def perform_create(self, serializer):
        user = self.request.user
        workspace = serializer.validated_data["workspace"]
        user_role = UserWorkspaceRole.objects.filter(
            user=user, workspace=workspace
        ).first()

        if user_role and user_role.role == "Admin":
            serializer.save()
        else:
            raise PermissionError(
                "You do not have permission to create tasks in this workspace."
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance.workspace
        ).first()

        if user_role and user_role.role == "Admin":
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You do not have permission to update this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance.workspace
        ).first()

        if user_role and user_role.role == "Admin":
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You do not have permission to delete this task."},
                status=status.HTTP_403_FORBIDDEN,
            )


class SubTaskViewSet(ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerailizer
    authentication_classes = [Auth]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_workspace_roles = UserWorkspaceRole.objects.filter(user=user)
        workspace_ids = user_workspace_roles.values_list("workspace_id", flat=True)
        task_ids = Task.objects.filter(workspace_id__in=workspace_ids).values_list(
            "id", flat=True
        )
        return SubTask.objects.filter(task_id__in=task_ids)

    def perform_create(self, serializer):

        user = self.request.user
        task = serializer.validated_data["task"]
        user_role = UserWorkspaceRole.objects.filter(
            user=user, workspace=task.workspace
        ).first()

        if user_role and user_role.role == "Admin":
            serializer.save()
        else:
            raise PermissionError(
                "You do not have permission to create subtasks in this workspace."
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance.task.workspace
        ).first()

        if user_role and user_role.role == "Admin":
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You do not have permission to update this subtask."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance.task.workspace
        ).first()

        if user_role and user_role.role == "Admin":
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You do not have permission to delete this subtask."},
                status=status.HTTP_403_FORBIDDEN,
            )

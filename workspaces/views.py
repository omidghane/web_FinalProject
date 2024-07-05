from urllib import request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.auth import Auth

from .models import Workspace, UserWorkspaceRole
from .serializer import WorkspaceSerailizer

User = get_user_model()
class WorkSpaceViewSet(ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerailizer
    authentication_classes = [Auth]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter workspaces where the user has a role assigned
        user = self.request.user
        user_workspace_roles = UserWorkspaceRole.objects.filter(user=user)
        workspace_ids = user_workspace_roles.values_list('workspace_id', flat=True)
        return Workspace.objects.filter(id__in=workspace_ids)

    def perform_create(self, serializer):
        # Ensure that the user creating the workspace is set as Admin
        workspace = serializer.save()
        UserWorkspaceRole.objects.create(
            user=self.request.user if isinstance(self.request.user,User) else User.objects.get(id=self.request.user),
            workspace=workspace,
            role='Admin'
        )

    def update(self, request, *args, **kwargs):
        # Check if the user has permission to update the workspace
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance
        ).first()

        if user_role and user_role.role == 'Admin':
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to update this workspace."},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, *args, **kwargs):
        # Check if the user has permission to delete the workspace
        instance = self.get_object()
        user_role = UserWorkspaceRole.objects.filter(
            user=request.user, workspace=instance
        ).first()

        if user_role and user_role.role == 'Admin':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to delete this workspace."},
                status=status.HTTP_403_FORBIDDEN
            )

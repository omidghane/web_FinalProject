from rest_framework.serializers import ModelSerializer

from .models import UserWorkspaceRole, Workspace


class WorkspaceSerailizer(ModelSerializer):

    class Meta:
        model = Workspace
        fields = "__all__"


class UserWorkspaceRoleSerailizer(ModelSerializer):

    class Meta:
        model = UserWorkspaceRole
        fields = "__all__"

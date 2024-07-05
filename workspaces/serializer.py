from rest_framework.serializers import ModelSerializer

from users.serializers import CustomUserSerializer

from .models import UserWorkspaceRole, Workspace


class WorkspaceSerailizer(ModelSerializer):

    class Meta:
        model = Workspace
        fields = "__all__"
        # fields = ['id', 'name']


class UserWorkspaceRoleSerailizer(ModelSerializer):
    user = CustomUserSerializer

    class Meta:
        model = UserWorkspaceRole
        fields = "__all__"

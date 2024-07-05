from rest_framework.serializers import ModelSerializer

from .models import UserWorkspaceRole, Workspace
from users.serializers import CustomUserSerializer

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

from rest_framework.serializers import ModelSerializer

from workspaces.serializer import WorkspaceSerailizer

from .models import SubTask, Task


class TaskSerailizer(ModelSerializer):
    workspace = WorkspaceSerailizer()

    class Meta:
        model = Task
        fields = "__all__"


class SubTaskSerailizer(ModelSerializer):

    class Meta:
        model = SubTask
        fields = "__all__"

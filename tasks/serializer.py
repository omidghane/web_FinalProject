from rest_framework.serializers import ModelSerializer

from workspaces.serializer import WorkspaceSerailizer

from .models import SubTask, Task


class TaskSerailizer(ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        
    def to_representation(self, instance: Task):
        result =  super().to_representation(instance)
        result['workspace'] = WorkspaceSerailizer(instance.workspace).data
        return result


class SubTaskSerailizer(ModelSerializer):

    class Meta:
        model = SubTask
        fields = "__all__"

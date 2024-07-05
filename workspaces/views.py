import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Workspace


class WorkspaceView(View):
    def get(self, request, workspace_id=None):
        if workspace_id:
            workspace = get_object_or_404(Workspace, id=workspace_id)
            data = {
                "id": workspace.id,
                "name": workspace.name,
                "description": workspace.description,
                "created_at": workspace.created_at,
                "updated_at": workspace.updated_at,
            }
        else:
            workspaces = Workspace.objects.all()
            data = [
                {
                    "id": workspace.id,
                    "name": workspace.name,
                    "description": workspace.description,
                }
                for workspace in workspaces
            ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        workspace = Workspace.objects.create(
            name=data["name"], description=data.get("description")
        )
        return JsonResponse(
            {
                "id": workspace.id,
                "name": workspace.name,
                "description": workspace.description,
            }
        )

    def put(self, request, workspace_id):
        data = json.loads(request.body)
        workspace = get_object_or_404(Workspace, id=workspace_id)
        workspace.name = data.get("name", workspace.name)
        workspace.description = data.get("description", workspace.description)
        workspace.save()
        return JsonResponse(
            {
                "id": workspace.id,
                "name": workspace.name,
                "description": workspace.description,
            }
        )

    def delete(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        workspace.delete()
        return HttpResponse(status=204)

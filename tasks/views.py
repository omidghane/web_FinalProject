import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from users.models import User
from workspaces.models import Workspace

from .models import SubTask, Task


class TaskView(View):
    def get(self, request, task_id=None):
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "estimated_time": task.estimated_time,
                "actual_time": task.actual_time,
                "due_date": task.due_date,
                "priority": task.priority,
                "workspace": task.workspace.id,
                "assignee": task.assignee.id if task.assignee else None,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "image_url": task.image_url,
            }
        else:
            tasks = Task.objects.all()
            data = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "estimated_time": task.estimated_time,
                    "actual_time": task.actual_time,
                    "due_date": task.due_date,
                    "priority": task.priority,
                    "workspace": task.workspace.id,
                    "assignee": task.assignee.id if task.assignee else None,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "image_url": task.image_url,
                }
                for task in tasks
            ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        workspace = get_object_or_404(Workspace, id=data["workspace"])
        assignee = (
            get_object_or_404(User, id=data["assignee"])
            if data.get("assignee")
            else None
        )
        task = Task.objects.create(
            title=data["title"],
            description=data.get("description"),
            status=data["status"],
            estimated_time=data.get("estimated_time"),
            actual_time=data.get("actual_time"),
            due_date=data.get("due_date"),
            priority=data["priority"],
            workspace=workspace,
            assignee=assignee,
            image_url=data.get("image_url"),
        )
        return JsonResponse(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "estimated_time": task.estimated_time,
                "actual_time": task.actual_time,
                "due_date": task.due_date,
                "priority": task.priority,
                "workspace": task.workspace.id,
                "assignee": task.assignee.id if task.assignee else None,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "image_url": task.image_url,
            }
        )

    def put(self, request, task_id):
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=task_id)
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)
        task.estimated_time = data.get("estimated_time", task.estimated_time)
        task.actual_time = data.get("actual_time", task.actual_time)
        task.due_date = data.get("due_date", task.due_date)
        task.priority = data.get("priority", task.priority)
        if "workspace" in data:
            task.workspace = get_object_or_404(Workspace, id=data["workspace"])
        if "assignee" in data:
            task.assignee = get_object_or_404(User, id=data["assignee"])
        task.image_url = data.get("image_url", task.image_url)
        task.save()
        return JsonResponse(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "estimated_time": task.estimated_time,
                "actual_time": task.actual_time,
                "due_date": task.due_date,
                "priority": task.priority,
                "workspace": task.workspace.id,
                "assignee": task.assignee.id if task.assignee else None,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "image_url": task.image_url,
            }
        )

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return HttpResponse(status=204)


class SubTaskView(View):
    def get(self, request, subtask_id=None):
        if subtask_id:
            subtask = get_object_or_404(SubTask, id=subtask_id)
            data = {
                "id": subtask.id,
                "title": subtask.title,
                "is_completed": subtask.is_completed,
                "task": subtask.task.id,
                "assignee": subtask.assignee.id if subtask.assignee else None,
                "created_at": subtask.created_at,
                "updated_at": subtask.updated_at,
            }
        else:
            subtasks = SubTask.objects.all()
            data = [
                {
                    "id": subtask.id,
                    "title": subtask.title,
                    "is_completed": subtask.is_completed,
                    "task": subtask.task.id,
                    "assignee": subtask.assignee.id if subtask.assignee else None,
                    "created_at": subtask.created_at,
                    "updated_at": subtask.updated_at,
                }
                for subtask in subtasks
            ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=data["task"])
        assignee = (
            get_object_or_404(User, id=data["assignee"])
            if data.get("assignee")
            else None
        )
        subtask = SubTask.objects.create(
            title=data["title"],
            is_completed=data.get("is_completed", False),
            task=task,
            assignee=assignee,
        )
        return JsonResponse(
            {
                "id": subtask.id,
                "title": subtask.title,
                "is_completed": subtask.is_completed,
                "task": subtask.task.id,
                "assignee": subtask.assignee.id if subtask.assignee else None,
                "created_at": subtask.created_at,
                "updated_at": subtask.updated_at,
            }
        )

    def put(self, request, subtask_id):
        data = json.loads(request.body)
        subtask = get_object_or_404(SubTask, id=subtask_id)
        subtask.title = data.get("title", subtask.title)
        subtask.is_completed = data.get("is_completed", subtask.is_completed)
        if "task" in data:
            subtask.task = get_object_or_404(Task, id=data["task"])
        if "assignee" in data:
            subtask.assignee = get_object_or_404(User, id=data["assignee"])
        subtask.save()
        return JsonResponse(
            {
                "id": subtask.id,
                "title": subtask.title,
                "is_completed": subtask.is_completed,
                "task": subtask.task.id,
                "assignee": subtask.assignee.id if subtask.assignee else None,
                "created_at": subtask.created_at,
                "updated_at": subtask.updated_at,
            }
        )

    def delete(self, request, subtask_id):
        subtask = get_object_or_404(SubTask, id=subtask_id)
        subtask.delete()
        return HttpResponse(status=204)

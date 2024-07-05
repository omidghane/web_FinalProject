from django.urls import path

from .views import SubTaskView, TaskView

urlpatterns = [
    path("tasks/", TaskView.as_view(), name="task-list"),
    path("tasks/<int:task_id>/", TaskView.as_view(), name="task-detail"),
    path("subtasks/", SubTaskView.as_view(), name="subtask-list"),
    path("subtasks/<int:subtask_id>/", SubTaskView.as_view(), name="subtask-detail"),
]

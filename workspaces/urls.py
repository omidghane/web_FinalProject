from django.urls import path

from .views import WorkspaceView

urlpatterns = [
    path("workspaces/", WorkspaceView.as_view(), name="workspace-list"),
    path(
        "workspaces/<int:workspace_id>/",
        WorkspaceView.as_view(),
        name="workspace-detail",
    ),
]

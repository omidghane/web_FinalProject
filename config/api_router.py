from django.urls import include, path

urlpatterns = [
    path("users/", include("users.urls")),
    path("tasks/", include("tasks.urls"), name="user-tasks"),
    path("workspaces/", include("workspaces.urls"), name="user-workspaces"),
]

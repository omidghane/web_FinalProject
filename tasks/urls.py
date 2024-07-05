from rest_framework.routers import DefaultRouter

from .views import SubTaskViewSet, TaskViewSet

router = DefaultRouter()

router.register("tasks", TaskViewSet, basename="tasks")
router.register("subtasks", SubTaskViewSet, basename="subtasks")
urlpatterns = router.urls

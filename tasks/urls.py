from rest_framework.routers import DefaultRouter

from .views import SubTaskViewSet, TaskViewSet

router = DefaultRouter()

router.register("", TaskViewSet, basename="tasks")
router.register("sub", SubTaskViewSet, basename="subtasks")
urlpatterns = router.urls

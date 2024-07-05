from rest_framework.routers import DefaultRouter

from .views import SubTaskViewSet, TaskViewSet

router = DefaultRouter()


router.register("sub", SubTaskViewSet, basename="subtasks")
router.register("", TaskViewSet, basename="tasks")
urlpatterns = router.urls

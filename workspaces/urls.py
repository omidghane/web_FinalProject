from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WorkSpaceViewSet

router = DefaultRouter()

router.register("", WorkSpaceViewSet, basename="workspaces")
urlpatterns = router.urls

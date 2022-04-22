from django.urls import include, path
from rest_framework import routers

from apps.api.settings.viewsets.settings import SettingsViewSet

router = routers.DefaultRouter()
router.register("", SettingsViewSet, basename="settings")


urlpatterns = [
    path("", include(router.urls)),
]

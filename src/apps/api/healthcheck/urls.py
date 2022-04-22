from django.urls import path

from apps.api.healthcheck.viewsets.healthcheck import HealthCheckViewSet

urlpatterns = [
    path(
        "health/",
        HealthCheckViewSet.as_view(actions={"get": "health"}),
        name="healthcheck",
    )
]

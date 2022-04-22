from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("settings/", include("apps.api.settings.urls")),
    path("", include("apps.api.healthcheck.urls")),
]

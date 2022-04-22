from django.urls import path

from apps.admin.views.dynamic_config.dynamic_config_admin import DynamicConfigAdminView
from apps.admin.docs.admin import ApiDocView, ApiDocSpecView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("api/docs/", login_required(ApiDocView.as_view()), name="api-docs"),
    path(
        "api/docs/specs/",
        login_required(ApiDocSpecView.as_view()),
        name="api-docs-specs",
    ),
    path("settings/", DynamicConfigAdminView.as_view(), name="dynamic-config"),
]

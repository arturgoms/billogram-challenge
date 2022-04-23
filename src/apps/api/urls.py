from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("settings/", include("apps.api.settings.urls")),
    path('user/', include('apps.api.user.urls')),
    path('brand/', include('apps.api.brand.urls')),
    path('brands/', include('apps.api.brands.urls')),
    path('discount/', include('apps.api.discount.urls')),
    path("", include("apps.api.healthcheck.urls")),
]

from django.urls import include, path

from apps.api.brand.viewsets.profile import BrandProfileViewSet
from commons.api.routers import ProfileRouter

profile_router = ProfileRouter()
profile_router.register("", BrandProfileViewSet, basename="brand-profile")

urlpatterns = [
    path("me/", include(profile_router.urls)),
]

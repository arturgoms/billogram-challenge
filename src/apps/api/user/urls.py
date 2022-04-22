from django.urls import include, path
from rest_framework import routers

from apps.api.user.viewsets.profile import UserProfileViewSet
from commons.api.routers import ProfileRouter

profile_router = ProfileRouter()
profile_router.register("", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("me/", include(profile_router.urls)),
]

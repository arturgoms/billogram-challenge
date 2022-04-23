from django.urls import include, path

from apps.api.user.viewsets.discounts import UserDiscountViewSet
from apps.api.user.viewsets.profile import UserProfileViewSet
from commons.api.routers import ProfileRouter
from rest_framework import routers


router = routers.DefaultRouter()
router.register("discounts", UserDiscountViewSet, basename="user-discount-list")

profile_router = ProfileRouter()
profile_router.register("", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("me/", include(profile_router.urls)),
    path("", include(router.urls)),
]

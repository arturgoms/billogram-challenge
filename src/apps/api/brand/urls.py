from django.urls import include, path

from apps.api.brand.viewsets.create_discount import CreateDiscountViewSet
from apps.api.brand.viewsets.discount_history import BrandDiscountHistoryViewSet
from apps.api.brand.viewsets.discounts import BrandDiscountViewSet
from apps.api.brand.viewsets.profile import BrandProfileViewSet
from apps.api.brand.viewsets.update_discount import BrandDiscountUpdateViewSet
from commons.api.routers import ProfileRouter
from rest_framework import routers


router = routers.DefaultRouter()
router.register("discounts", BrandDiscountViewSet, basename="brand-discount")

profile_router = ProfileRouter()
profile_router.register("", BrandProfileViewSet, basename="brand-profile")

urlpatterns = [
    path("me/", include(profile_router.urls)),
    path("discount/<uuid:pk>/", BrandDiscountUpdateViewSet.as_view(actions={"put": "partial_update"}), name="brand-discount"),
    path("discount/<uuid:pk>/history", BrandDiscountHistoryViewSet.as_view(actions={"get": "list"}), name="brand-discount"),
    path("discount/", CreateDiscountViewSet.as_view(actions={"post": "create"}), name="brand-discount"),
    path("", include(router.urls)),
]

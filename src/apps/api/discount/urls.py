from django.urls import include, path
from rest_framework import routers

from apps.api.discount.viewsets.list import DiscountListViewSet
from apps.api.discount.viewsets.fetch import DiscountFetchViewSet

router = routers.DefaultRouter()
router.register("", DiscountListViewSet, basename="discount-list")

urlpatterns = [
    path(
        "<uuid:pk>/",
        DiscountFetchViewSet.as_view(actions={"get": "fetch"}),
        name="discount-fetch",
    ),
    path("", include(router.urls)),
]

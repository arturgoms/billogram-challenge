from django.urls import include, path

from rest_framework import routers

from apps.api.brands.viewsets.brands import BrandsListViewSet

router = routers.DefaultRouter()
router.register("", BrandsListViewSet, basename="brands-list")


urlpatterns = [
    path("", include(router.urls)),
]

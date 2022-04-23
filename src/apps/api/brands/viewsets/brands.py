import uuid
from apps.api import permissions
from apps.api.brands.serializers.brands import BrandsSerializer
from apps.domain import models
from commons.api import viewsets
from commons.djutils.api.mixins import FilterQuerysetMixin
from commons.djutils.models.filters import Search
from commons.models import filters


class BrandsListViewSet(FilterQuerysetMixin, viewsets.ListModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = BrandsSerializer
    permission_classes = [permissions.IsUser]

    filters = [
        filters.Filter('ids', lookup='pk', cast=uuid.UUID, many=True),
        filters.Filter('website', lookup='website', cast=str, many=True),
        Search(lookups=['name__icontains'])
    ]

    def get_queryset(self):
        return super().get_queryset()

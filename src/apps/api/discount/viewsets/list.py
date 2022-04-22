import uuid

from commons.djutils.api.mixins import FilterQuerysetMixin

from apps.api.discount.serializers.list import DiscountSerializer
from apps.domain import models
from commons.api import viewsets
from commons.api.permissions import IsAuthenticated
from commons.djutils.models.filters import Search
from commons.models import filters


class DiscountListViewSet(FilterQuerysetMixin, viewsets.ListModelViewSet):
    queryset = models.Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    filters = [
        filters.Filter('ids', lookup='pk', cast=uuid.UUID, many=True),
        filters.Filter('brand_website', lookup='brand__website', cast=str, many=True),
        filters.Filter('brand', lookup='brand__name', cast=str, many=True),
        Search(lookups=['description__icontains'])
    ]

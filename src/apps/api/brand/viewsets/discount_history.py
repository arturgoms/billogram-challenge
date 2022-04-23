import uuid
from apps.api import permissions
from apps.api.brand.serializers.discount_history import DiscountsHistorySerializer
from apps.domain import models
from commons.api import viewsets
from commons.djutils.api.mixins import FilterQuerysetMixin
from commons.models.filters import Filter


class BrandDiscountHistoryViewSet(FilterQuerysetMixin, viewsets.ListModelViewSet):
    queryset = models.UserDiscount.objects.all()
    serializer_class = DiscountsHistorySerializer
    permission_classes = [permissions.IsBrand]

    filters = [
        Filter('ids', lookup='pk', cast=uuid.UUID, many=True)
    ]

    def get_queryset(self):
        return super().get_queryset() \
            .filter(discount_id=self.kwargs.get('pk'))

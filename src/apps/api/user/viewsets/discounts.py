import uuid
from apps.api import permissions
from apps.api.user.serializers.discounts import DiscountsSerializer
from apps.domain import models
from commons.api import viewsets
from commons.djutils.api.mixins import FilterQuerysetMixin
from commons.models.filters import Filter


class UserDiscountViewSet(FilterQuerysetMixin, viewsets.ListModelViewSet):
    queryset = models.UserDiscount.objects.all()
    serializer_class = DiscountsSerializer
    permission_classes = [permissions.IsUser]

    filters = [
        Filter('ids', lookup='pk', cast=uuid.UUID, many=True)
    ]

    def get_queryset(self):
        return super().get_queryset() \
            .filter(user_id=self.request.user.pk)

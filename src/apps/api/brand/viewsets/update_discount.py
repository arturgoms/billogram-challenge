from django.shortcuts import get_object_or_404

from apps.api import permissions
from apps.api.brand.serializers.update_discount import BrandChangeDiscountSerializer
from commons.api import viewsets, mixins
from apps.domain import models


class BrandDiscountUpdateViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Discount.objects.all()
    update_serializer_class = BrandChangeDiscountSerializer
    serializer_class = BrandChangeDiscountSerializer
    permission_classes = [permissions.IsBrand]

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

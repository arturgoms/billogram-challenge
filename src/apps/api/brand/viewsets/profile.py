from django.shortcuts import get_object_or_404

from apps.api import permissions
from apps.api.brand.serializers.profile import BrandProfileSerializer
from apps.domain import models
from commons.api import viewsets, mixins


class BrandProfileViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = BrandProfileSerializer
    permission_classes = [permissions.IsBrand]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_object(self):
        """
        Returns the current logged student to be serialized.
        """
        return get_object_or_404(self.get_queryset(), pk=self.request.user.pk)

    def discounts_queryset_resolver(self, queryset):  # noqa
        """
        Optimize partial load from ``lessons`` field into
        serialized response.
        """
        return queryset.include_discounts()

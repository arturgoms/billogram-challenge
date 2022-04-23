from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class BrandSerializer(PartialModelSerializer):
    class Meta:
        model = models.Brand
        fields = ["id", "website", "name", "email"]


class DiscountSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False)

    class Meta:
        model = models.Discount
        fields = ["id", "brand", "description"]

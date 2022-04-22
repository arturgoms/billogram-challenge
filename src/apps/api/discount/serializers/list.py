from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class DiscountsSerializer(PartialModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['id', 'website', 'name', 'email']


class DiscountSerializer(serializers.ModelSerializer):
    brand = DiscountsSerializer(many=False)

    class Meta:
        model = models.Discount
        fields = ['id', 'brand', 'description']

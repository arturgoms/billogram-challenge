from rest_framework import serializers
from apps.domain import models


class BrandChangeDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = ["id", "code", "description", "quantity", "hide", "enable"]
        read_only_fields = ["id", "brand"]

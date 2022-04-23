from rest_framework import serializers
from apps.domain import models


class CreateDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = ["id", "code", "description", "quantity", "hide", "enable"]
        read_only_fields = ["id", "brand"]

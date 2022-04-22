from rest_framework import serializers
from apps.domain import models


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Discount
        fields = ['id', 'code', 'description']

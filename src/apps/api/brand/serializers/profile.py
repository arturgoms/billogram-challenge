from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class BrandChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['website', 'name']


class DiscountsSerializer(PartialModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj): # noqa
        balance_qs = models.UserDiscount.objects.filter(discount_id=obj.id).count()
        balance = obj.quantity - balance_qs
        return balance

    class Meta:
        model = models.Discount
        fields = ['id', 'code', 'description', 'quantity', 'balance']


class BrandProfileSerializer(serializers.ModelSerializer):
    discounts = DiscountsSerializer(source='brand_discount', many=True)

    class Meta:
        model = models.Brand
        fields = ['id', 'website', 'name', 'email', 'discounts']
        read_only_fields = ['id', 'email', 'discount']

from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class DiscountsSerializer(PartialModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj): # noqa
        balance_qs = models.UserDiscount.objects.filter(discount_id=obj.id).count()
        balance = obj.quantity - balance_qs
        return balance

    class Meta:
        model = models.Discount
        fields = ['id', 'code', 'description', 'quantity', 'balance', 'hide', 'enable']

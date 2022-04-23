from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class DiscountSerializer(PartialModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):  # noqa
        balance_qs = models.UserDiscount.objects.filter(discount_id=obj.id).count()
        balance = obj.quantity - balance_qs
        return balance

    class Meta:
        model = models.Discount
        fields = ["id", "code", "description", "quantity", "balance", "hide", "enable"]


class UserSerializer(PartialModelSerializer):
    class Meta:
        model = models.User
        fields = ["first_name", "email"]


class DiscountsHistorySerializer(PartialModelSerializer):
    discount = DiscountSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = models.UserDiscount
        fields = ["id", "discount", "user"]

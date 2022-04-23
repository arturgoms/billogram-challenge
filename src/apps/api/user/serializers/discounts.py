from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class BrandSerializer(PartialModelSerializer):
    class Meta:
        model = models.Brand
        fields = ["id", "name", "website"]


class DiscountSerializer(PartialModelSerializer):
    brand = BrandSerializer(many=False)

    class Meta:
        model = models.Discount
        fields = ["id", "code", "description", "brand"]


class DiscountsSerializer(PartialModelSerializer):
    discount = DiscountSerializer(many=False)

    class Meta:
        model = models.UserDiscount
        fields = ["id", "discount"]

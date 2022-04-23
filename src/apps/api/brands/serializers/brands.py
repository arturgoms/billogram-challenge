from apps.domain import models
from commons.api.serializers import PartialModelSerializer


class BrandsSerializer(PartialModelSerializer):

    class Meta:
        model = models.Brand
        fields = ['id', 'name', 'website']

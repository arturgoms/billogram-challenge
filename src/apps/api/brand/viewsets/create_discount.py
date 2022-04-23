from apps.api.brand.serializers.create_discount import CreateDiscountSerializer
from commons.api import viewsets, mixins
from apps.api import permissions
from rest_framework import status
from apps.domain import models
from rest_framework.response import Response


class CreateDiscountViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateDiscountSerializer
    permission_classes = [permissions.IsBrand]

    def create(self, request, *args, **kwargs):
        serializer = CreateDiscountSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        instance = models.Discount.objects.create(
            code=serializer.validated_data['code'],
            description=serializer.validated_data['description'],
            quantity=serializer.validated_data['quantity'],
            hide=serializer.validated_data['hide'],
            enable=serializer.validated_data['enable'],
        )

        serializer = self.get_serializer(instance=instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

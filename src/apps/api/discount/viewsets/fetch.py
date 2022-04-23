from apps.api.discount.serializers.fetch import DiscountSerializer
from rest_framework import viewsets, status

from apps.api import permissions
from apps.domain import models
from commons.api.mixins import RetrieveModelMixin
from rest_framework.response import Response


class DiscountFetchViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Discount.objects.all()
    permission_classes = [permissions.IsUser]
    serializer_class = DiscountSerializer

    def fetch(self, request, *args, **kwargs):

        # Check if user already fetch the discount
        if models.UserDiscount.objects.filter(
            user_id=request.user.pk, discount_id=self.kwargs.get("pk")
        ).exists():
            return Response(
                {"error": "User already get that discount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TODO: check if the balance is greater then 0
        # TODO: check if discount is enabled

        models.UserDiscount.objects.create(
            discount_id=self.kwargs.get("pk"), user_id=request.user.pk
        )

        instance = models.Discount.objects.get(id=self.kwargs.get("pk"))

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from apps.api.discount.serializers.fetch import DiscountSerializer
from rest_framework import viewsets, status

from apps.api import permissions
from apps.domain import models
from commons.api.mixins import RetrieveModelMixin
from rest_framework.response import Response
from apps.worker import tasks


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

        discount = models.Discount.objects.get(pk=self.kwargs.get("pk"))
        if not discount.enable:
            return Response(
                {"error": "This discount is disable, sorry."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        user_discount = models.UserDiscount.objects.filter(discount=discount).count()
        if discount.quantity - user_discount == 0:
            return Response(
                {"error": "This discount is not available anymore, sorry."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        tasks.send_notification.apply_async(
            kwargs={
                "user": models.User.objects.get(id=request.user.pk).full_name,
                "discount": discount.code,
                "brand": discount.brand.name,
            }
        )

        models.UserDiscount.objects.create(
            discount_id=self.kwargs.get("pk"), user_id=request.user.pk
        )

        instance = models.Discount.objects.get(id=self.kwargs.get("pk"))

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

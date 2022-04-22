from functools import partial
from rest_framework import serializers

from apps.domain import models
from commons.api.serializers import modelserializer_factory


class UserChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    discount = modelserializer_factory(
        models.UserDiscount,
        fields=['id', 'code', 'brand'],
        read_only=True,
        field_classes={
            'id': partial(serializers.UUIDField, source='discount.id'),
            'code': partial(serializers.CharField, source='discount.code'),
            'brand': partial(serializers.UUIDField, source='discount.brand')
        }, many=True)

    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'discount']
        read_only_fields = ['id', 'email', 'discount']

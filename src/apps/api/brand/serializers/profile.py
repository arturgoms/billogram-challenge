from rest_framework import serializers
from apps.domain import models


class BrandProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ["id", "website", "name", "email"]
        read_only_fields = ["id", "email"]

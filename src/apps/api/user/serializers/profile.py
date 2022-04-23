from rest_framework import serializers
from apps.domain import models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'email']

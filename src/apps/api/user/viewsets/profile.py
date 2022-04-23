from django.shortcuts import get_object_or_404

from apps.api import permissions
from apps.api.user.serializers.profile import UserProfileSerializer
from apps.domain import models
from commons.api import viewsets, mixins


class UserProfileViewSet(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = models.User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsUser]

    def get_object(self):
        """
        Returns the current logged student to be serialized.
        """
        return get_object_or_404(self.get_queryset(), pk=self.request.user.pk)

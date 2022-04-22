from django.http import HttpResponse
from rest_framework import viewsets, status


class HealthCheckViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []

    def health(self, request, *args, **kwargs):  # noqa
        """
        Returns whether the service is health.
        """

        return HttpResponse(
            "Healthy", content_type="text/plain", status=status.HTTP_200_OK
        )

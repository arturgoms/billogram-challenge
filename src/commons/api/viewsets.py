from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin

from commons.api import mixins


class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = (
            kwargs.pop("serializer_class", None) or self.get_serializer_class()
        )
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class ListModelViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides default `list()` action.
    """


class CreateModelViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    A viewset that provides default `create()` action.
    """


class RetrieveModelViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    A viewset that provides default `retrieve()` action.
    """


class UpdateModelViewSet(mixins.UpdateModelMixin, GenericViewSet):
    """
    A viewset that provides default `update()` action.
    """


class DestroyModelViewSet(mixins.DestroyModelMixin, GenericViewSet):
    """
    A viewset that provides default `destroy()` action.
    """


class ReadOnlyModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """


class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

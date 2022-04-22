import re

from django.utils.functional import cached_property
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


def _resolve(*fields, tree=None):
    tree = tree or {}

    for field in fields:
        field, *nested = field

        if not nested:
            tree[field] = None
            continue

        tree[field] = _resolve(nested, tree=tree.get(field, {}))

    return tree


def resolve_fields(fields):
    return _resolve(*map(lambda x: x.strip().split("."), fields.split(",")))


class PartialViewSetMixin:
    fields_url_kwarg = "fields"
    resolver_suffix = "queryset_resolver"

    @cached_property
    def partial_fields(self):
        fields = self.request.GET.get(self.fields_url_kwarg)

        if not fields:
            return None

        return resolve_fields(fields)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["fields"] = self.partial_fields
        return context

    def _get_field_resolvers(self, field):
        """
        Returns all specific field resolvers to nested fields.
        """
        nested_re = re.compile(
            r"{field}_(.+)_{suffix}".format(field=field, suffix=self.resolver_suffix)
        )

        return filter(lambda x: bool(nested_re.match(x)), dir(self))

    def resolve_queryset_fields(self, queryset, fields, prefix=None):
        prefix = prefix or ""

        for field, nested in fields.items():
            field = f"{prefix}_{field}" if prefix else field
            resolver = getattr(self, f"{field}_{self.resolver_suffix}", None)

            if resolver is not None:
                queryset = resolver(queryset)

            if not nested:

                for resolver in self._get_field_resolvers(field):
                    queryset = getattr(self, resolver)(queryset)

                continue

            queryset = self.resolve_queryset_fields(queryset, nested, prefix=field)

        return queryset

    def resolve_all_fields(self, queryset):
        for resolver in filter(lambda x: x.endswith("_queryset_resolver"), dir(self)):
            resolver = getattr(self, resolver)
            queryset = resolver(queryset)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.partial_fields:
            return self.resolve_queryset_fields(queryset, self.partial_fields)

        return self.resolve_all_fields(queryset)


class CreateModelMixin:
    """
    Create a model instance.
    """

    create_serializer_class = None
    create_response_serializer_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, serializer_class=self.create_serializer_class
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # prepare response.
        serializer = self.get_serializer(
            instance=serializer.instance,
            serializer_class=self.create_response_serializer_class,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    list_response_serializer_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, serializer_class=self.list_response_serializer_class
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, serializer_class=self.list_response_serializer_class
        )
        return Response(serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    retrieve_response_serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, serializer_class=self.retrieve_response_serializer_class
        )
        return Response(serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    update_serializer_class = None
    update_response_serializer_class = None

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            serializer_class=self.update_serializer_class,
        )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            setattr(instance, "_prefetched_objects_cache", {})

        serializer = self.get_serializer(
            instance=instance, serializer_class=self.update_response_serializer_class
        )
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

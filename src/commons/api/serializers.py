from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class Serializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DatePeriodSerializer(Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if validated_data["start_date"] > validated_data["end_date"]:
            raise serializers.ValidationError(
                {
                    "start_date": _(
                        "The 'start_date' must be less than or equal to 'end_date'."
                    )
                }
            )

        return validated_data


class PartialSerializerMixin:
    @property
    def _readable_fields(self):
        """
        Returns only fields defined in the context
        or the complete serializer.
        """
        _cached_prop = "__readable_fields"

        if not hasattr(self, _cached_prop):
            readable_fields = getattr(super(), "_readable_fields")
            context = getattr(self, "_context")

            fields = context.get("fields")

            if not fields:
                # it is not a partial response
                return readable_fields

            partial_fields = list(
                filter(lambda x: x.field_name in fields, readable_fields)
            )

            for field in partial_fields:
                field_context = context.copy()
                field_context.update({"fields": fields.get(field.field_name)})

                setattr(field, "_context", field_context)

                if hasattr(field, "child"):
                    setattr(field.child, "_context", field_context.copy())

            setattr(self, _cached_prop, partial_fields)

        return getattr(self, _cached_prop)


class PartialModelSerializer(PartialSerializerMixin, serializers.ModelSerializer):
    """
    Provides support to partial serializer.
    """


class URLField(serializers.URLField):
    """
    A field that automatically convert partial urls to absolute one.
    """

    def to_representation(self, value):
        request = self.context.get("request")
        value = super().to_representation(value)

        if not request:
            return value

        return request.build_absolute_uri(value)


class MediaURLField(serializers.URLField):
    """
    A field that automatically convert a media path to absolute url.
    """

    def __init__(self, **kwargs):
        storage = kwargs.pop("storage", None)
        super().__init__(**kwargs)
        self.storage = storage or default_storage

    def to_representation(self, value):
        request = self.context.get("request")
        value = super().to_representation(value)

        if not value:
            return None

        value = self.storage.url(value)

        if not request:
            return value

        return request.build_absolute_uri(value)


class NestedSerializerField(serializers.Field):  # noqa
    """
    A read-only field that get its representation from a given serializer
    class based on parent serializer class and a resolver that
    get a single instance as a parameter.
    """

    def __init__(self, serializer_class, resolver, **kwargs):
        self.resolver = resolver
        self.serializer_class = serializer_class
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        value = self.resolver(value)

        if not value:
            return None

        serializer = self.serializer_class(value, context=self.parent.context)
        return serializer.data

    def to_internal_value(self, data):
        return data


def modelserializer_class_factory(
    model, fields, read_only=False, serializer=None, field_classes=None, meta=None
):
    """
    Return a ModelSerializer containing form fields for the given model. You can
    optionally pass a `serializer` argument to use as a starting point for
    constructing the ModelSerializer.
    """
    serializer = serializer or serializers.ModelSerializer
    class_name = model.__name__ + "Serializer"

    meta_class = type(
        "Meta",
        (object,),
        {
            "model": model,
            "fields": fields,
            "read_only_fields": None if not read_only else fields,
            **(meta or {}),
        },
    )

    serializer_class_attrs = {
        "Meta": meta_class,
        **{
            field_name: field_class()
            for field_name, field_class in (field_classes or {}).items()
        },
    }

    return type(serializer)(class_name, (serializer,), serializer_class_attrs)


def modelserializer_factory(
    model,
    fields,
    read_only=False,
    serializer=None,
    field_classes=None,
    meta=None,
    **kwargs
):
    """
    Return a ModelSerializer containing form fields for the given model. You can
    optionally pass a `serializer` argument to use as a starting point for
    constructing the ModelSerializer.
    """
    serializer_class = modelserializer_class_factory(
        model=model,
        fields=fields,
        read_only=read_only,
        serializer=serializer,
        field_classes=field_classes,
        meta=meta,
    )

    return serializer_class(**kwargs)

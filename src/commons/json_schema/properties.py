import inspect

from commons.json_schema.base import JsonSchema, BaseProperty
from commons.json_schema.factory import jsonschema_factory


class ObjectProperty(BaseProperty):
    type = "object"

    def __init__(self, title=None, description=None, schema=None, **kwargs):
        super().__init__(title, description, **kwargs)

        if inspect.isclass(schema) and issubclass(schema, JsonSchema):
            schema = schema()

        elif isinstance(schema, dict):
            schema = jsonschema_factory(schema)

        self.schema = schema

    def to_dict(self):
        schema = self.schema.to_dict() if self.schema else {}

        for key, val in super().to_dict().items():
            schema[key] = val

        return schema


class StringProperty(BaseProperty):
    type = "string"

    FORMAT_EMAIL = "email"
    FORMAT_URI = "uri"
    FORMAT_DATE = "date"
    FORMAT_TIME = "time"
    FORMAT_DATETIME = "date-time"

    def __init__(
        self,
        title=None,
        description=None,
        format=None,
        pattern=None,
        min_length=None,
        max_length=None,
        **kwargs
    ):
        super().__init__(title, description, **kwargs)
        self.format = format
        self.pattern = pattern
        self.min_length = min_length
        self.max_length = max_length

    def to_dict(self):
        schema = super().to_dict()

        if self.format:
            schema["format"] = self.format

        if self.pattern:
            schema["pattern"] = self.pattern

        if self.min_length is not None:
            schema["minLength"] = self.min_length

        if self.max_length is not None:
            schema["maxLength"] = self.max_length

        return schema


class RegexProperty(StringProperty):
    def __init__(self, title=None, description=None, pattern=None, **kwargs):
        super().__init__(title, description, pattern=pattern, **kwargs)


class DateProperty(StringProperty):
    def __init__(self, title=None, description=None, **kwargs):
        kwargs.setdefault("format", StringProperty.FORMAT_DATE)
        super().__init__(title, description, **kwargs)


class TimeProperty(StringProperty):
    def __init__(self, title=None, description=None, **kwargs):
        kwargs.setdefault("format", StringProperty.FORMAT_TIME)
        super().__init__(title, description, **kwargs)


class DateTimeProperty(StringProperty):
    def __init__(self, title=None, description=None, **kwargs):
        kwargs.setdefault("format", StringProperty.FORMAT_DATETIME)
        super().__init__(title, description, **kwargs)


class EmailProperty(StringProperty):
    def __init__(self, title=None, description=None, **kwargs):
        kwargs.setdefault("format", StringProperty.FORMAT_EMAIL)
        super().__init__(title, description, **kwargs)


class UUIDProperty(RegexProperty):
    UUID_RE = (
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )

    def __init__(self, title=None, description=None, **kwargs):
        super().__init__(title, description, pattern=UUIDProperty.UUID_RE, **kwargs)


class UriProperty(StringProperty):
    def __init__(self, title=None, description=None, **kwargs):
        kwargs.setdefault("format", StringProperty.FORMAT_URI)
        super().__init__(title, description, **kwargs)


class IntegerProperty(BaseProperty):
    type = "integer"


class NumberProperty(BaseProperty):
    type = "number"


class BooleanProperty(BaseProperty):
    type = "boolean"


class ArrayProperty(BaseProperty):
    type = "array"

    def __init__(
        self,
        title=None,
        description=None,
        items=None,
        min_items=None,
        max_items=None,
        additional_items=None,
        **kwargs
    ):
        super().__init__(title, description, **kwargs)
        _items = []

        for item in items if isinstance(items, (list, tuple)) else [items]:
            if inspect.isclass(item) and issubclass(item, JsonSchema):
                item = item()

            elif isinstance(item, dict):
                item = jsonschema_factory(item)

            _items.append(item)

        assert all(
            isinstance(item, (BaseProperty, JsonSchema)) for item in _items
        ), "The 'items' must be instance of BaseProperty or JsonSchema."

        self._items = _items
        self.max_items = max_items
        self.min_items = min_items
        self.additional_items = additional_items

    @property
    def items(self):
        items = [item.to_dict() for item in self._items]
        return items[0] if len(items) == 1 else items

    def to_dict(self):
        schema = super().to_dict()

        if self.items:
            schema["items"] = self.items

        if self.min_items is not None:
            schema["minItems"] = self.min_items

        if self.max_items is not None:
            schema["maxItems"] = self.max_items

        if self.additional_items is not None:
            schema["additionalItems"] = self.additional_items

        return schema


class MixedTypeProperty(BaseProperty):
    def __init__(self, title=None, description=None, types=None, **kwargs):
        super().__init__(title=title, description=description, **kwargs)
        self.type = [item.type for item in types]

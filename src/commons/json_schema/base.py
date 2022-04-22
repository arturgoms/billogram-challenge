# pylint: skip-file
import collections
import json

import jsonschema


def validate_schema(schema, data):
    """
    Validates whether the data is valid based on schema.
    """
    if isinstance(schema, JsonSchema):
        schema = schema.to_dict()

    try:
        jsonschema.validate(data, schema)

    except jsonschema.ValidationError:
        return False

    else:
        return True


class BaseProperty:
    type = None

    def __init__(
        self,
        title=None,
        description=None,
        default=None,
        examples=None,
        nullable=False,
        required=True,
    ):
        self.title = title
        self.description = description
        self.default = default
        self.examples = examples
        self.required = required
        self.nullable = nullable

    def to_dict(self):
        if self.nullable and isinstance(self.type, (list, tuple)):
            type_ = list(self.type) + ["null"]

        elif self.nullable:
            type_ = [self.type, "null"]

        else:
            type_ = self.type

        return collections.OrderedDict(
            filter(
                lambda x: x[1] is not None,
                [
                    ("type", type_),
                    ("title", self.title),
                    ("description", self.description),
                    ("examples", self.examples),
                    ("default", self.default),
                ],
            )
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.type}>"

    def __str__(self):
        return self.to_json()


class JsonSchemaOptions:
    def __init__(self):
        self.additional_properties = True
        self.title = None
        self.description = None
        self.properties = []

    @classmethod
    def init(cls, **kwargs):
        instance = cls()

        for key, val in kwargs.items():
            setattr(instance, key, val)

        return instance


class JsonSchemaMeta(type):
    @classmethod
    def _get_declared_properties(mcs, bases, attrs):
        properties = [
            (name, prop)
            for name, prop in attrs.items()
            if isinstance(prop, BaseProperty)
        ]

        # If this class is subclassing another Schema, add that Schema's
        # properties. Note that we loop over the bases in *reverse*. This is necessary
        # in order to maintain the correct order of fields.
        for base in reversed(bases):
            opts = getattr(base, "_meta", None)

            if not opts or not opts.properties:
                continue

            properties = [
                (name, prop)
                for name, prop in opts.properties.items()
                if name not in attrs
            ] + properties

        return collections.OrderedDict(properties)

    def __new__(mcs, name, bases, attrs, **kwargs):
        attr_meta = (attrs.pop("Meta", None) or object).__dict__.items()
        meta = JsonSchemaOptions.init(
            **{key: val for key, val in attr_meta if not key.startswith("_")}
        )
        meta.properties = mcs._get_declared_properties(bases, attrs)
        attrs["_meta"] = meta
        return super().__new__(mcs, name, bases, attrs, **kwargs)

    def __iter__(cls):
        """
        Implicit instantiate the class when try to iter.
        """
        return iter(cls())  # pylint: disable=no-value-for-parameter


class JsonSchema(metaclass=JsonSchemaMeta):
    def to_dict(self):
        opts = getattr(self, "_meta")
        properties = opts.properties.items()
        return collections.OrderedDict(
            filter(
                lambda x: x[1] is not None,
                [
                    ("type", "object"),
                    ("title", opts.title),
                    ("description", opts.description),
                    ("properties", {name: prop.to_dict() for name, prop in properties}),
                    ("required", [name for name, prop in properties if prop.required]),
                    ("additionalProperties", opts.additional_properties),
                ],
            )
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def is_valid(self, data):
        """
        Validates whether the data is valid based on schema.
        """
        data = json.loads(data) if isinstance(data, str) else data
        return validate_schema(self.to_dict(), data)

    def __iter__(self):
        for item in self.to_dict().items():
            yield item

    def __repr__(self):
        opts = getattr(self, "_meta")
        properties = list(opts.properties.values())
        return f"<({type(self).__name__}): {properties}>"

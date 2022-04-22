import copy

from commons.json_schema.base import JsonSchema


def _generate_property(prop, required=False):
    from commons.json_schema import properties

    properties_type_map = {
        "string": properties.StringProperty,
        "number": properties.NumberProperty,
        "integer": properties.IntegerProperty,
        "boolean": properties.BooleanProperty,
    }

    nullable = False
    prop_type = prop.pop("type", None)

    if isinstance(prop_type, (list, tuple)):
        nullable = "null" in prop_type
        prop_type = list(filter(lambda x: x != "null", prop_type))[0]

    base_attrs = {
        "title": prop.pop("title", None),
        "description": prop.pop("description", None),
        "examples": prop.pop("examples", None),
        "default": prop.pop("default", None),
        "nullable": nullable,
        "required": required,
    }

    if prop_type == "object":
        return properties.ObjectProperty(schema=jsonschema_factory(prop), **base_attrs)

    if prop_type == "array":
        items = prop.pop("items", [])

        if not isinstance(items, (list, tuple)):
            items = [items]

        return properties.ArrayProperty(
            **{
                "items": list(map(_generate_property, items)),
                "additional_items": prop.pop("additionalItems", False),
                "max_items": prop.pop("maxItems", None),
                "min_items": prop.pop("minItems", None),
                **base_attrs,
            }
        )

    return properties_type_map[prop_type](**{**base_attrs, **prop})


def jsonschema_factory(schema):
    schema = copy.deepcopy(schema)

    meta = type(
        "Meta",
        (),
        {
            "title": schema.get("title"),
            "description": schema.get("description"),
            "additional_properties": schema.get("additionalProperties"),
        },
    )

    required = set(schema.get("required") or [])

    attrs = {
        name: _generate_property(prop, required=name in required)
        for name, prop in (schema.get("properties") or {}).items()
    }

    attrs["Meta"] = meta

    return type("JsonSchema", (JsonSchema,), attrs)()

import collections

from commons.string import camel_case_to_snake_case


def flatten_map(mapping, parent_key=None, sep="_"):
    """
    Flat nested mapping keys into a single level.
    """
    items = []

    for key, val in mapping.items():
        new_key = parent_key + sep + key if parent_key else key

        if isinstance(val, collections.Mapping):
            items.extend(flatten_map(val, new_key, sep=sep).items())

        else:
            items.append((new_key, val))

    return dict(items)


def camel_case_map_parser(mapping):
    """
    Converts CamelCase keys into snake case.
    """
    items = []

    for key, val in mapping.items():
        key = camel_case_to_snake_case(key)

        if isinstance(val, collections.Mapping):
            val = camel_case_map_parser(val)

        items.append((key, val))

    return dict(items)

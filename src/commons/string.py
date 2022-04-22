import functools


def camel_case_to_snake_case(string):
    """
    Convert string from CamelCase to snake_case.
    """
    return functools.reduce(
        lambda a, b: f"{a}_{b}" if b.isupper() else f"{a}{b}", string
    ).lower()

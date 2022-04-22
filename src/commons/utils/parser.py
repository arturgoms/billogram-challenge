class Undefined:
    """
    Sentinel object to control values cast.
    """

    def __call__(self, value):
        """
        Do not perform any changes on value.
        """
        return value


# Reference instance to represent undefined values
undefined = Undefined()


def boolean(value):
    """
    Special cast bound to bool type.
    """
    value = str(value).lower()

    if value in ("y", "yes", "t", "true", "on", "1"):
        value = True

    elif value in ("n", "no", "f", "false", "off", "0"):
        value = False

    else:
        raise ValueError(f"invalid value for bool(): '{value}'")

    return value


class csv:  # noqa
    __slots__ = ("delimiter",)

    def __init__(self, delimiter=","):
        self.delimiter = delimiter

    def __call__(self, value):
        """
        Split value into a parameter list.
        """
        if not value:
            return []

        return list(filter(None, (v.strip(" ") for v in value.split(self.delimiter))))


def parse(value, cast=undefined):
    """
    Parse value based on a cast function:
    """
    cast = cast if cast is not bool else boolean
    return cast(value)

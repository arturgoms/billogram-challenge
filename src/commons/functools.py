# pylint: skip-file


class cached_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    A cached property can be made out of an existing method:
    (e.g. ``url = cached_property(get_absolute_url)``).
    """

    name = None

    def __init__(self, func):
        self.func = func
        self.__doc__ = getattr(func, "__doc__")

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance ``_cached_NAME`` attribute
        so that subsequent attribute access on the instance returns the cached value
        instead of calling the function again.
        """
        if instance is None:
            return self

        _cached_prop = f"_cached_{self.name}"

        if not hasattr(instance, _cached_prop):
            setattr(instance, _cached_prop, self.func(instance))

        return getattr(instance, _cached_prop)

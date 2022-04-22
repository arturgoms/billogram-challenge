import warnings


def deprecated(function=None, message=None):
    """
    Can be used to mark functions as deprecated. It will result
    in a warning being emitted when the function is used.
    """

    def decorator(func):
        warning = "{} is deprecated. {}".format(func.__name__, message or "")

        def decorated(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)  # turn off filter
            warnings.warn(warning, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)  # reset filter
            return func(*args, **kwargs)

        return decorated

    if function is None:
        return decorator

    return decorator(function)

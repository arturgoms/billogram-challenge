from typing import Mapping, Sequence


class ObjectDict(Mapping):
    """
    Provides the ability to handle a Mapping as a Object.
    """

    def __init__(self, data):
        assert isinstance(data, Mapping), "parameter 'data' must be a mapping type"
        self._mapping = data

    def _get_value(self, key):
        """
        Get mapping value from key.
        """
        value = self._mapping[key]

        if isinstance(value, Mapping):
            # Grant the object behavior to nested mappings.
            value = ObjectDict(value)

        elif isinstance(value, Sequence) and not isinstance(value, str):
            # Grant the object behavior to mappings inside a sequence.
            value = [ObjectDict(v) if isinstance(v, dict) else v for v in value]

        return value

    def get(self, key, default=None):
        try:
            value = self._get_value(key)

        except KeyError:
            return default

        else:
            return value

    def __getitem__(self, item):
        return self._get_value(item)

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __repr__(self):
        return f"{type(self).__name__}({self._mapping})"

    def __getattr__(self, item):
        """
        Tries to return a object attribute or a object key.
        """
        try:
            return self.__getattribute__(item)

        except AttributeError:
            try:
                return self._get_value(item)

            except KeyError:
                raise AttributeError(
                    "type object '{name}' has no attribute {attr}".format(
                        name=self.__class__.__name__, attr=item
                    )
                )

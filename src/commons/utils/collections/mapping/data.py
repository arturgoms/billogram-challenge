from typing import Mapping, Sequence

from commons.utils import parser


class DataDict(Mapping):
    def __init__(self, data):
        assert isinstance(data, Mapping), "parameter 'data' must be a mapping type"
        self.mapping = data

    def get(self, key, default=None, cast=parser.undefined):

        try:
            value = parser.parse(self.mapping[key], cast=cast)

        except (KeyError, ValueError, TypeError):
            return default

        else:
            return value

    def __getitem__(self, item):
        return self.mapping[item]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"{type(self).__name__}({self.mapping})"

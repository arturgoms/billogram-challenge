import functools
import operator as op

from django.db.models import Q
from commons.djutils.models import filters
from commons.utils import parser
from commons.utils.collections import DataDict


def get_multi_value_lookup(
    request,
    url_kwarg,
    lookup_field=None,
    many=False,
    delimiter=",",
    operator=op.or_,
    cast=parser.undefined,
):
    """
    Generate the lookups for a field with a given request.

    Returns None if no field is provided.
    """
    lookup_field = lookup_field or url_kwarg
    values = DataDict(request.GET).get(
        url_kwarg, default=[], cast=parser.csv(delimiter=delimiter)
    )

    _filters = []

    for value in values:
        try:
            _filters.append(parser.parse(value, cast=cast))

        except (KeyError, ValueError, TypeError):
            continue

    # remove duplicated values.
    _filters = list(set(_filters))

    if not many:
        _filters = _filters[:1]

    if not _filters:
        return None

    return functools.reduce(
        operator, map(lambda x: Q(**{lookup_field: x}), _filters), Q()
    )


class Filter(filters.BaseFilter):
    def __init__(
        self,
        url_kwarg,
        lookup=None,
        many=False,
        delimiter=",",
        operator=op.or_,
        default=filters.unset,
        distinct=False,
        cast=parser.undefined,
    ):
        super().__init__(url_kwarg)

        self.lookup = lookup or url_kwarg
        self.many = many
        self.delimiter = delimiter
        self.operator = operator
        self.cast = cast
        self.default = default
        self.distinct = distinct

    def filter(self, request, queryset):
        lookup = (
            get_multi_value_lookup(
                request=request,
                url_kwarg=self.url_kwarg,
                lookup_field=self.lookup,
                many=self.many,
                delimiter=self.delimiter,
                operator=self.operator,
                cast=self.cast,
            )
            or self.default
        )

        if lookup is filters.unset:
            return queryset

        queryset = queryset.filter(lookup)

        if self.distinct or self.many:
            queryset = queryset.distinct()

        return queryset

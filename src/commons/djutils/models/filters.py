import functools
import operator
from typing import Sequence

from django.db.models import Q
from commons.utils import parser
from commons.utils.collections import DataDict


class Unset:
    """
    Class to represent an unset instance.
    """

    def __bool__(self):
        # always returns false in a boolean conversion.
        return False


unset = Unset()


class BaseFilter:
    """
    Define the filter object with expected features.
    """

    def __init__(self, url_kwarg):
        self.url_kwarg = url_kwarg

    def value(self, request):
        """
        Returns the value from lookup kwarg.
        """
        return request.GET.get(self.url_kwarg, None)

    def filter(self, request, queryset):
        """
        This method must implement a way to handle the queryset
        and apply the filter.

        Args:
            request: (view.Request, required) - The view request.
            queryset: (models.Queryset, required) - Queryset to be filtered.

        Returns:
            Queryset object.
        """
        raise NotImplementedError('The "filter" method must be implemented.')

    def __call__(self, request, queryset):
        return self.filter(request, queryset)


class Filter(BaseFilter):
    def __init__(
        self,
        url_kwarg,
        lookup=None,
        default=unset,
        distinct=False,
        cast=parser.undefined,
    ):
        super().__init__(url_kwarg)

        self.lookup = lookup or url_kwarg
        self.cast = cast
        self.default = default
        self.distinct = distinct

    def value(self, request):
        return DataDict(request.GET).get(self.url_kwarg, self.default, cast=self.cast)

    def filter(self, request, queryset):
        value = self.value(request)

        if value is unset:
            return queryset

        queryset = queryset.filter(**{self.lookup: value})

        if self.distinct:
            queryset = queryset.distinct()

        return queryset


class ChoiceFilter(Filter):
    """
    Filter the queryset based on a available choice.
    """

    def __init__(self, url_kwarg, choices, *args, **kwargs):
        super().__init__(url_kwarg, *args, **kwargs)

        if isinstance(choices, Sequence):
            self.choices = {v: v for v in choices}

        self.choices = choices

    def value(self, request):
        value = super().value(request)
        return self.choices.get(value, unset)


class Search(BaseFilter):
    def __init__(self, lookups, url_kwarg="query", distinct=False):
        super().__init__(url_kwarg)

        self.lookups = lookups
        self.distinct = distinct

    def filter(self, request, queryset):
        value = self.value(request)

        if not value:
            return queryset

        queryset = queryset.filter(
            functools.reduce(operator.or_, map(lambda x: Q(**{x: value}), self.lookups))
        )

        if self.distinct:
            queryset = queryset.distinct()

        return queryset

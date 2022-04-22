from abc import ABCMeta

from django.db import models


class SubqueryAvg(models.Subquery, metaclass=ABCMeta):
    template = '(SELECT AVG("%(field)s") FROM (%(subquery)s) AS "_avg")'
    output_field = models.FloatField()

    def __init__(self, queryset, field, *args, **kwargs):
        queryset = queryset.values(field)
        super().__init__(queryset, field=field, *args, **kwargs)

    def resolve_expression(self, *args, **kwargs):
        # As a performance optimization, remove ordering since COUNT doesn't
        # care about it, just whether or not a row matches.
        self.query.clear_ordering(force_empty=True)
        return super().resolve_expression(*args, **kwargs)


class SubqueryCount(models.Subquery, metaclass=ABCMeta):
    template = '(SELECT COUNT(*) FROM (%(subquery)s) AS "_count")'
    output_field = models.IntegerField()

    def __init__(self, queryset, *args, fields=None, **kwargs):
        queryset = queryset.values(*(fields or ["id"]))
        super().__init__(queryset, *args, **kwargs)

    def resolve_expression(self, *args, **kwargs):
        # As a performance optimization, remove ordering since COUNT doesn't
        # care about it, just whether or not a row matches.
        self.query.clear_ordering()
        return super().resolve_expression(*args, **kwargs)

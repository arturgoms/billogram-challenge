from django.db import models


class SubqueryCount(models.Subquery):  # noqa
    template = '(SELECT COUNT(*) FROM (%(subquery)s) AS "_count")'
    output_field = models.IntegerField()

    def __init__(self, queryset, *args, fields=None, **kwargs):
        queryset = queryset.values(*(fields or ["id"]))
        super().__init__(queryset, *args, **kwargs)

    def resolve_expression(self, query=None, *args, **kwargs):
        # As a performance optimization, remove ordering since COUNT doesn't
        # care about it, just whether or not a row matches.
        self.queryset = self.queryset.order_by()
        return super().resolve_expression(query, *args, **kwargs)

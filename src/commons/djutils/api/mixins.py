from django.core.exceptions import ImproperlyConfigured

from commons.djutils.models.shortcuts import filter_queryset, sort_queryset


class CallableQuerysetMixin:
    """
    Mixin for handle a callable queryset,
    which will force the update of the queryset.
    Related to issue http://code.djangoproject.com/ticket/8378
    """

    queryset = None

    def get_queryset(self):
        """
        Check that the queryset is defined and call it.

        Returns:
            models.db.QuerySet
        """
        cls = type(self)

        if self.queryset is None:
            raise ImproperlyConfigured(f"'{cls.__name__}' must define 'queryset'")

        return self.queryset()  # pylint: disable=E1102


class FilterQuerysetMixin:
    """
    Mixin to apply filters to the queryset.
    """

    filters = None

    def get_filters(self):
        """
        Returns all filter instances for this view.

        Returns:
            list
        """
        return self.filters or []

    def filter_queryset(self, queryset):
        """
        After the base handle of the view into queryset, apply
        view custom filters to modify the queryset.

        Args:
            queryset (models.db.Queryset, required): Queryset to apply filters.

        Returns:
            models.db.Queryset
        """
        queryset = super().filter_queryset(queryset)
        return filter_queryset(self.request, queryset, self.filters)


class SortQuerysetMixin:
    """
    Mixin for handling a queryset and sort it
    """

    sortable_fields = None
    sort_url_kwarg = "sort"

    def get_sortable_fields(self):
        """
        Returns all sortable fields for this view.

        Returns:
            list
        """
        return self.sortable_fields or []

    def get_sort_url_kwarg(self):
        """
        Returns all sortable fields for this view.

        Returns:
            str
        """
        return self.sort_url_kwarg

    def sort_queryset(self, queryset):
        """
        Sort queryset.

        Args:
            queryset (models.db.Queryset, required): Queryset to apply sort.

        Returns:
            models.db.Queryset
        """
        return sort_queryset(
            self.request,
            queryset,
            sortable_fields=self.get_sortable_fields(),
            sort_url_kwarg=self.get_sort_url_kwarg(),
        )

    def filter_queryset(self, queryset):
        """
        After the base handle of the view into queryset, apply custom sort.

        Args:
            queryset (models.db.Queryset, required): Queryset to apply sort.

        Returns:
            models.db.Queryset
        """
        return self.sort_queryset(super().filter_queryset(queryset))

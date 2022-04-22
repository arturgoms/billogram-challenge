from django.core.paginator import Paginator
from django.db.models import OrderBy, F
from commons.utils import parser
from commons.utils.collections import DataDict, first_or_default


def paginate_queryset(request, queryset, page_size=None, paginator_cls=None):
    """
    Paginate a given queryset based on request parameters.

    Args:
        request (Request, required): Http Request object.
        queryset (django.db.models.QuerySet, required): Queryset to be listed.
        page_size (int, optional): Number of items per page. Default: 10.
        paginator_cls (django.core.paginator.Paginator, optional): Pagination to paginate queryset.

    Returns:
        django.core.paginator.Page
    """
    paginator_cls = paginator_cls or Paginator

    query = DataDict(request.GET)
    page_size = page_size or query.get("page_size", default=10, cast=int)
    page_number = query.get("page", default=1, cast=int)

    return paginator_cls(queryset, per_page=page_size).page(page_number)


def filter_queryset(request, queryset, filters):
    """
    Filter a given queryset based on provided model filters.

    Args:
        request (Request, required): Http Request object.
        queryset (django.db.models.QuerySet, required): Queryset to be listed.
        filters (list, required): Filter list to apply into queryset.

    Returns:
        django.db.models.QuerySet
    """
    for func in filters:
        queryset = func(request, queryset)

    return queryset


def sort_queryset(request, queryset, sortable_fields, sort_url_kwarg="sort"):
    """
    Sort a given queryset based on provided sort fields.

    Args:
        request (Request, required): Http Request object.
        queryset (django.db.models.QuerySet, required): Queryset to be listed.
        sortable_fields (list, required): Sort fields to apply into queryset.
        sort_url_kwarg (str, optional): Request sort parameter name.
            Default: ``sort``.

    Returns:
        django.db.models.QuerySet

    Example:
        >>> sort_queryset(request, queryset, sortable_fields=[
        >>>    'title',
        >>>    ('description', {
        >>>        'nulls_first': True
        >>>    })
        >>> ])
    """
    sortable_fields = dict(
        map(lambda x: (x, {}) if isinstance(x, str) else (x[0], x[1]), sortable_fields)
    )
    fields = []

    for field in DataDict(request.GET).get(sort_url_kwarg, cast=parser.csv()) or []:
        field_name = field.lstrip("-")

        if field_name not in sortable_fields:
            continue

        fields.append(
            (
                field_name,
                {
                    **sortable_fields.get(field_name, {}),
                    "descending": field.startswith("-"),
                },
            )
        )

    if not fields:
        return queryset

    return queryset.order_by(*[OrderBy(F(field), **opts) for field, opts in fields])


def get_model_field(model, field_name):
    """
    Returns the field class from model.

    Args:
        model (django.db.Model, required): Model to retrieve the field.
        field_name: (str, required): Field name.

    Returns:
        models.db.Field
    """
    opts = getattr(model, "_meta")
    return first_or_default(
        opts.fields, func=lambda x: x.name == field_name, default=None
    )

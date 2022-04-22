from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


def get_list_response(request, queryset, serializer_cls, paginator_cls=None):
    """
    Returns a list response.

    Args:
        request (Request, required): Http Request object.
        queryset (django.db.models.QuerySet, required): Queryset to be listed.
        serializer_cls (rest_framework.serializers.Serializer, required): Serializer to serialize objects.
        paginator_cls (rest_framework.pagination.BasePagination, optional): Pagination to paginate queryset.

    Returns:
        rest_framework.response.Response
    """
    paginator_cls = paginator_cls or api_settings.DEFAULT_PAGINATION_CLASS
    page = (
        paginator_cls().paginate_queryset(queryset, request)
        if paginator_cls is not None
        else None
    )

    if page is not None:
        serializer = serializer_cls(page, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = serializer_cls(queryset, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

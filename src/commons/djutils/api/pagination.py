from collections import OrderedDict

from django.core.paginator import Paginator as BasePaginator
from commons.utils.collections import DataDict
from rest_framework.pagination import PageNumberPagination, BasePagination
from rest_framework.response import Response
from rest_framework.settings import api_settings


class Paginator(BasePaginator):
    """
    Add support to return all items from database
    by passing ``per_page`` equals to -1.
    """

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

        # returns all items if ``per_page`` is -1
        self.per_page = self.count if per_page == -1 else per_page
        self.per_page = (self.per_page or api_settings.PAGE_SIZE) or 10


class DefaultPagination(PageNumberPagination):
    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = "page_size"

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = None

    # If enabled, returns all records in a single page. It must be used carefully to not
    # overload the server.
    ALL = -1

    # Uses a special paginator capable to handle all records in a single page.
    django_paginator_class = Paginator

    def get_page_size(self, request):
        """
        Grant ability to return the whole database items by
        passing the url query ``page_size=-1``.

        Args:
            request (Request, required): Request object.

        Returns:
            int
        """
        page_size = DataDict(request.query_params).get(
            self.page_size_query_param, default=None, cast=int
        )

        if page_size == DefaultPagination.ALL:
            # -1 returns all records.
            return -1

        return super().get_page_size(request)


class SkipPagination(BasePagination):
    def to_html(self):
        """
        Ignored to avoid django rest layout errors.

        Returns:
            str
        """
        return ""

    def paginate_queryset(self, queryset, request, view=None):
        """
        Ignore pagination returning the whole queryset.

        Args:
            queryset (django.db.Queryset, required): Queryset object.
            request (Request, required): Request object.
            view (django.views.generic.base.View, optional): View that is handling the queryset.

        Returns:
            list
        """
        return list(queryset)

    def get_paginated_response(self, data):
        """
        Create default paginated response for non-paginated queryset.

        Args:
            data (Any, required): Data to be returned.

        Returns:
            rest_framework.response.Response
        """
        return Response(OrderedDict([("results", data)]))

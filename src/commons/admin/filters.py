from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ImproperlyConfigured


class RelatedFilter(SimpleListFilter):
    related_queryset = None
    required_parameter_names = None

    def get_related_queryset(self, request):
        """
        Returns the queryset to the filter.
        """
        if self.related_queryset is None:
            raise ImproperlyConfigured(
                "Missing ``related_queryset`` attribute on %s" % self.__class__.__name__
            )

        queryset = self.related_queryset

        lookups = {
            key: request.GET.get(key) for key in (self.required_parameter_names or [])
        }

        if not all(lookups.values()):
            return queryset.none()

        queryset = queryset.filter(**lookups)

        return queryset

    def get_lookup_text(self, obj):  # noqa
        """
        Returns lookup text label.
        """
        return str(obj)

    def lookups(self, request, model_admin):
        """
        Yields each lookup found in queryset.
        """
        queryset = self.get_related_queryset(request)

        if queryset.count() == 1:
            # only display with at least 2 lookups.
            return

        for obj in queryset:
            yield str(obj.pk), self.get_lookup_text(obj)

    def queryset(self, request, queryset):
        """
        Applies queryset filter.
        """
        value = self.value()

        return queryset.filter(**{self.parameter_name: value if value != "-" else None})


class HiddenFilter(SimpleListFilter):
    parameter_name = None

    def lookups(self, request, model_admin):
        return None

    def queryset(self, request, queryset):
        value = self.value()

        if not value or value == "-":
            # skip filter
            return queryset

        return queryset.filter(**{self.parameter_name: value})

    @classmethod
    def create(cls, parameter_name, **kwargs):
        """
        Returns the class with field defined.
        """
        # returns modified class.
        return type(
            "SimpleFilter",
            (cls,),
            {**kwargs, "title": "", "parameter_name": parameter_name},
        )

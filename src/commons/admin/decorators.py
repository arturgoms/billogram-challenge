from rest_framework.exceptions import PermissionDenied


def admin_view(route=None, name=None, detail=True, permission=lambda request: True):
    def wrap(func):
        """
        Wraps the function to add meta information
        to resolve the view and register
        the url.
        """

        def wrapped_view(self, request, *args, **kwargs):
            if not permission(request):
                raise PermissionDenied()
            return func(self, request, *args, **kwargs)

        wrapped_view.name = name or func.__name__.replace("_view", "").replace("_", "-")
        wrapped_view.route = route
        wrapped_view.detail = detail
        wrapped_view.is_extra_view = True
        return wrapped_view

    return wrap


def admin_changelist_widget(title=None, template=None):
    def wrap(func):
        """
        Add required meta information.
        """
        func.title = title
        func.template = template
        func.is_changelist_widget = True
        return func

    return wrap


def admin_action(short_description=None):
    def wrap(func):
        """
        Wraps the function to add meta information
        to admin action.
        """
        name = func.__name__.replace("_action", "").replace("_", " ")
        func.short_description = short_description or name
        func.is_extra_action = True
        return func

    return wrap


def admin_field(short_description=None, boolean=False):
    def wrap(func):
        """
        Wraps the function to add meta information
        to resolve a field property
        on admin site.
        """

        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)

            if result in ("", None):
                return "-"

            return result

        wrapped.short_description = short_description or func.__name__.replace(
            "_field", ""
        )
        wrapped.boolean = boolean
        return wrapped

    return wrap

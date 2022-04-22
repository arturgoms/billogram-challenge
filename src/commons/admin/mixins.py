import inspect
from functools import update_wrapper

from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html_join, format_html
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe


def partial_call(func, **kwargs):
    """
    Call the function only with its required arguments.
    """
    return func(
        **{
            key: value
            for key, value in kwargs.items()
            if key in inspect.getfullargspec(func).args
        }
    )


class AdminActionMixin:
    def get_extra_actions(self):
        """
        Walk through the class methods to identify
        which are extra actions and
        return them.
        """
        actions = []

        for name in filter(lambda x: x.endswith("_action"), dir(self)):
            # get only actions names with the suffix `_action`.
            func = getattr(self, name)

            if not getattr(func, "is_extra_action", False):
                # ignores if the function was not wrapped
                # by @admin_action decorator.
                continue

            actions.append((func, name, func.short_description))

        return actions

    def _get_base_actions(self):
        """
        Return both base actions and extra actions.
        """
        actions = super()._get_base_actions()

        # join base actions and extra actions.
        return list(actions) + self.get_extra_actions()


class AdminToolsMixin:
    """
    A mixin to provide the object tools buttons.

    Ex:
    >>> object_tools = {
    >>>     'changelist': [{
    >>>         'title': 'Button Title',
    >>>         'url': 'url/action/',
    >>>         'permission': 'path.to.permission.checker',
    >>>         'attrs': {'attr1': 'value'}
    >>>     }, {
    >>>         'title': 'Button Title',
    >>>         'url': lambda opts: 'url/action/',
    >>>         'permission': 'path.to.permission.checker',
    >>>         'attrs': {'attr1': 'value'}
    >>>     }],
    >>>     'change': [{
    >>>         'title': 'Button Title',
    >>>         'url': lambda opts, obj: 'url/action',
    >>>         'permission': 'path.to.permission.checker',
    >>>         'attrs': {'attr1': 'value'}
    >>>     }]
    >>> }
    """

    object_tools = None

    def has_tool_permission(self, permission, request, obj=None):
        """
        Check if the permission was granted.
        """
        if not permission:
            return True

        if not callable(permission):
            # try to get the permission
            permission = import_string(permission)

        return partial_call(permission, request=request, obj=obj)

    def get_tool_title(self, title):
        """
        Returns the title based on model meta information.
        """
        return title % {
            "verbose_name": self.opts.verbose_name,
            "verbose_name_plural": self.opts.verbose_name_plural,
            "app_label": self.opts.app_label,
        }

    def render_group(self, request, title, items, attrs=None, obj=None):
        """
        Render the whole group of tools.
        """
        items = (
            partial_call(items, request=request, obj=obj, opts=self.opts)
            if callable(items)
            else None
        )

        tpl = (
            '<li class="dropdown"><a title="{title}" data-toggle="dropdown" href="#"{attrs}>{title}</a>'
            '<ul class="dropdown-menu">{items}</ul></li>'
        )

        # render all items
        rendered_tools = list(
            filter(None, [self.render_tool(request, obj=obj, **tool) for tool in items])
        )

        if not rendered_tools:
            # if any item has permission or the list is empty,
            # then ignore this tool.
            return None

        return tpl.format(
            title=self.get_tool_title(title),
            attrs=format_html_join("", ' {}="{}"', (attrs or {}).items()),
            items="".join(rendered_tools),
        )

    def render_tool(self, request, title, url, permission=None, attrs=None, obj=None):
        """
        Returns a rendered tool button based on the data.
        """
        tpl = '<li><a title="{title}" href="{url}"{attrs}>{title}</a></li>'

        # if has no permission return None
        if not self.has_tool_permission(permission, request, obj):
            return None

        if callable(url):
            try:
                url = partial_call(url, request=request, opts=self.opts, obj=obj)

            except TypeError:
                return ""

        attrs = attrs or {}

        return tpl.format(
            title=self.get_tool_title(title),
            url=url,
            attrs=format_html_join("", ' {}="{}"', attrs.items()),
        )

    def get_object_tools(self, request, view_name, obj=None):
        """
        Returns a object tool list for required view.
        """
        output = []

        if not self.object_tools:
            return output

        # get all tools for view.
        tools = self.object_tools.get(view_name, [])

        # Render each tool according with type and permission.
        rendered_tools = []

        for tool in tools:
            if "items" in tool:
                rendered_tool = self.render_group(request, obj=obj, **tool)
            else:
                rendered_tool = self.render_tool(request, obj=obj, **tool)

            if not rendered_tool:
                continue

            rendered_tools.append(mark_safe(rendered_tool))

        # returns only rendered tools which
        # has permission.
        return rendered_tools

    def changelist_view(self, request, extra_context=None):
        """
        Add the changelist object tools to context.
        """
        extra_context = extra_context or {}
        extra_context["object_tools"] = self.get_object_tools(request, "changelist")
        return super().changelist_view(request, extra_context)

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        """
        Add the change form object tools context.
        """
        if obj is not None:
            context["object_tools"] = self.get_object_tools(request, "change", obj)

        return super().render_change_form(
            request=request,
            context=context,
            add=add,
            change=change,
            form_url=form_url,
            obj=obj,
        )


class AdminViewMixin:

    extra_views = []

    def get_extra_views(self):
        """
        Walk into current class and get all extra views.
        """
        if self.extra_views:
            # if the extra view was defined manually,
            # consider it's more important than walking
            # in the class to discovery views.
            return [getattr(self, view_name) for view_name in self.extra_views]

        extra_views = []

        for view_name in filter(lambda x: x.endswith("_view"), dir(self)):
            # get only views names with the suffix `_view`.
            view_func = getattr(self, view_name)

            if not getattr(view_func, "is_extra_view", False):
                # ignores if the function was not wrapped
                # by @admin_view decorator.
                continue

            extra_views.append(view_func)

        return extra_views

    def get_extra_view(self, view):
        """
        Handle the current view to add custom
        information to register in
        admin site urls.
        """
        # resolve the current view name.
        name = getattr(view, "name", None) or view.__name__.replace(
            "_view", ""
        ).replace("_", "-")

        # resolve the current view route.
        route = getattr(view, "route", None) or ("%s/" % name)

        if getattr(view, "detail", False):
            # add object_id argument if the view is a detail view.
            route = "<path:object_id>/{route}/".format(
                route=route.rstrip("/").lstrip("/")
            )

        def wrap(func):
            """
            Wraps current view as admin view.
            """

            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            # define current admin as the model admin instance.
            wrapper.model_admin = self

            # returns the wrapped view
            return update_wrapper(wrapper, func)

        # returns the wrapped view, name and route
        # from this routes.
        return wrap(view), name, route

    def get_extra_urls(self):
        opts = getattr(self.model, "_meta")
        app_label = opts.app_label
        model_name = opts.model_name

        urlpatterns = []

        for view in self.get_extra_views():
            view, name, route = self.get_extra_view(view)

            urlpatterns.append(
                path(route, view, name="%s_%s_%s" % (app_label, model_name, name))
            )

        return urlpatterns

    def get_urls(self):
        urlpatterns = super().get_urls()
        extra_urlpatterns = self.get_extra_urls()
        return extra_urlpatterns + urlpatterns


class SmartAdminMixin(AdminActionMixin, AdminToolsMixin, AdminViewMixin):
    """
    Add support to AdminActionMixin, AdminToolsMixin and AdminViewMixin.
    """

    def redirect(self, request, next_url, message, level, params=None):
        """
        Redirect to next url with a related message.
        """
        self.message_user(request, format_html(message, **(params or {})), level=level)
        return HttpResponseRedirect(next_url)

    def log_change(self, request, object, message, params=None):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """

        if not isinstance(message, list):
            message = format_html(message, **(params or {}))

        return super().log_change(request, object, message)

    def log_addition(self, request, object, message, params=None):
        """
        Log that an object has been successfully added.

        The default implementation creates an admin LogEntry object.
        """
        if not isinstance(message, list):
            message = format_html(message, **(params or {}))

        return super().log_addition(request, object, message)

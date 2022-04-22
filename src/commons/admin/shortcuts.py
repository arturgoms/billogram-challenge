from django.urls import reverse
from django.utils.functional import lazy
from django.utils.html import format_html
from commons.utils.string import pluralize

from commons.admin.settings import ADMIN_SHORTCUTS
from commons.admin.utils import call_from_string
from commons.urls import querystring


def admin_url(view_name, opts, args=None, kwargs=None, params=None):
    """
    Reverse a url to admin site using the provided args.
    """
    view_name = "admin:%s_%s_%s" % (opts.app_label, opts.model_name, view_name)

    # get url for the view.
    url = reverse(view_name, args=args, kwargs=kwargs)

    # returns the url adding the querystring params.
    return querystring(url, includes=params)


admin_url_lazy = lazy(admin_url, str)


def get_readonly_fields(fieldsets, exclude=None):
    """
    Returns all fieldset fields as readonly.
    """
    exclude = exclude or []

    fields = []

    for fieldset in fieldsets:
        fields += [field for field in fieldset[1]["fields"] if field not in exclude]

    return fields


def get_related_model_count_link(model, count, lookup_filter):
    """
    Returns a link or a text of a related model count.
    """
    if not count > 0:
        return "-"

    _opts = getattr(model, "_meta")

    display_text = pluralize(
        f"{count} {_opts.verbose_name}", f"{count} {_opts.verbose_name_plural}", count
    )

    url = querystring(admin_url("changelist", _opts), includes=lookup_filter)

    return format_html('<a href="{}">{}</a>', url, display_text)


class Shortcut:
    """
    Renders a shortcut button to
    django admin site.
    """

    def __init__(self, request, title, url, icon=None, perm=None):
        self.request = request
        self.title = title
        self.url = url
        self._icon = icon
        self.perm = perm

    @property
    def is_active(self):
        """
        Check if the current url matches with
        this shortcut url.
        """
        return self.request.path.startswith(str(self.url))

    def has_perm(self):
        """
        Verify if the panel_user has permission to view
        the shortcut.
        """
        has_perm = False

        if not self.perm:
            # grant permission for shortcuts without
            # defined perm.
            has_perm = True

        elif callable(self.perm):
            # test the permission function and
            # returns the result.
            has_perm = self.perm(self.request)

        elif isinstance(self.perm, str):
            # import the permission checker from
            # string and test it.
            has_perm = call_from_string(self.perm, request=self.request)

        elif isinstance(self.perm, bool):
            # returns the defined permission
            has_perm = self.perm

        # otherwise do not grant the permission.
        return has_perm

    @property
    def icon(self):
        """
        Renders the icon to show on admin shortcut.
        """
        if not self._icon:
            return ""

        icon_type = self._icon.pop("type", "icon")

        if icon_type == "img":
            # returns a rendered image icon.
            return format_html(
                '<img src="{url}" class="shortcut-icon" />', **self._icon
            )

        # returns a rendered font-awesome icon.
        return format_html(
            '<i class="shortcut-icon {prefix} fa-fw fa-{name}"></i>',
            **{**self._icon, "prefix": self._icon.get("prefix", "fa")},
        )

    def render(self):
        """
        Returns the rendered shortcut button.
        """
        icon = self.icon

        if icon:
            # shows the icon if necessary.
            content = format_html(
                '{icon} <span class="shortcut-title">{title}</span>',
                icon=icon,
                title=self.title,
            )
        else:
            # get the content without the title.
            content = format_html(
                '<span class="shortcut-title">{title}</span>', title=self.title
            )

        return format_html(
            '<a href="{url}" class="shortcut{active}">{content}</a>',
            content=content,
            url=self.url,
            active="" if not self.is_active else " active",
        )


def admin_shortcuts(request):
    """
    Returns all shortcuts from admin site.
    """
    if not ADMIN_SHORTCUTS:
        # If admin shortcuts was not configured
        # just ignore.
        return []

    # creates a instance for each defined shortcut.
    shortcuts = [Shortcut(request, **shortcut) for shortcut in ADMIN_SHORTCUTS]

    # returns only shortcuts with permission.
    return filter(lambda x: x.has_perm(), shortcuts)

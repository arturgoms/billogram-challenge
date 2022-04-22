import inspect

from django import template as django_template
from django.conf import settings
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.utils.module_loading import import_string

from commons.admin.groups import resolve_registered_groups
from commons.admin.settings import ADMIN_USER_LINKS
from commons.admin.shortcuts import admin_shortcuts

register = django_template.Library()


@register.simple_tag(name="version")
def do_version(*args, **kwargs):
    """
    Returns the current application version.
    """
    version = getattr(settings, "VERSION", "1.0.0")
    return f"v{version}"


@register.inclusion_tag(
    "admin/tags/dummy.html", name="admin_shortcuts", takes_context=True
)
def do_admin_shortcuts(context, template="admin/tags/shortcuts.html"):
    """
    Returns a rendered template with admin shortcuts.
    """
    request = context.get("request")

    return {
        "template": template,
        "shortcuts": admin_shortcuts(request),
        "request": request,
    }


@register.simple_tag(name="admin_groups", takes_context=True)
def do_admin_groups(context, *args, **kwargs):
    from django.contrib.admin.sites import site as default_site

    return resolve_registered_groups(request=context.get("request"), site=default_site)


@register.simple_tag(name="admin_languages", takes_context=True)
def do_admin_languages(context, *args, **kwargs):
    request = context.get("request")
    path = request.get_full_path().split("/", 2)[-1]
    languages = []

    for code, label in settings.LANGUAGES:
        languages.append({"url": f"/{code}/{path}", "code": code, "label": label})

    return languages


@register.inclusion_tag(
    "admin/tags/dummy.html", name="changelist_widget", takes_context=True
)
def do_changelist_widget(context, widget):
    """
    Render all widget in a list.
    """
    request = context.get("request")

    return {**widget, "request": request}


@register.simple_tag(name="get_user_links", takes_context=True)
def do_get_user_links(context):
    """
    Return all user links.
    """
    links = []

    for link in ADMIN_USER_LINKS or []:
        permission = link.get("permission")

        if isinstance(permission, str):
            permission = import_string(permission)

        if callable(permission):
            func = inspect.getfullargspec(permission)
            kwargs = {}

            if "request" in func.args:
                kwargs["request"] = context.get("request")

            if not permission(**kwargs):
                continue

        links.append(link)

    return links


@register.tag(name="custom_submit_row")
def custom_submit_row_tag(parser, token):
    node = InclusionAdminNode(
        parser,
        token,
        func=lambda context, template_name=None: submit_row(context),
        template_name="submit_line.html",
    )

    custom_template_name = node.kwargs.get("template_name")

    if custom_template_name:
        node.template_name = custom_template_name.resolve(None)

    return node

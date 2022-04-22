from django import template as django_template
from django.template import defaulttags
from django.template.base import Node, TemplateSyntaxError
from django.templatetags import static
from django.utils.safestring import mark_safe

from commons.urls import get_absolute_uri, querystring

register = django_template.Library()


@register.simple_tag(name="define")
def do_define(value):
    """
    Helper to define a variable in Django templates.
    """
    return value


class QuerystringNode(Node):
    def __init__(self, url, includes, excludes):
        self.url = url
        self.includes = includes
        self.excludes = excludes

    def resolve_kwargs(self, values, context):  # noqa
        """
        Resolve dict based values.
        """
        return {
            key.resolve(context): value.resolve(context)
            for key, value in values.items()
        }

    def resolve_args(self, values, context):  # noqa
        """
        Resolve list based values.
        """
        return [value.resolve(context) for value in values]

    def render(self, context):
        """
        Returns a modified URL based on include and exclude parameters.
        """
        return querystring(
            url=self.url.resolve(context),
            includes=self.resolve_kwargs(self.includes, context),
            excludes=self.resolve_args(self.excludes, context),
        )


@register.tag(name="querystring")
def do_querystring(parser, token):
    """
    Modify a URL including or excluding querystring parameters.

    >>> {% querystring '/some/url/?next=1' page=1 excludes 'next' %}
    """
    bits = token.split_contents()

    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' need url argument." % bits[0])

    includes, excludes = {}, []
    url = parser.compile_filter(bits[1])
    bits = bits[2:]

    try:
        exclude_index = bits.index("excludes")

        includes = bits[:exclude_index]
        excludes = bits[exclude_index + 1 :]

    except ValueError:
        includes = bits

    includes = filter(lambda x: len(x) == 2, map(lambda x: x.split("="), includes))

    return QuerystringNode(
        url,
        includes={
            parser.compile_filter(key): parser.compile_filter(val)
            for key, val in includes
        },
        excludes=map(parser.compile_filter, excludes),
    )


class AbsStaticNode(static.StaticNode):
    def url(self, context):
        return get_absolute_uri(super().url(context), request=context.get("request"))


@register.tag("abs_static")
def do_abs_static(parser, token):
    return AbsStaticNode.handle_token(parser, token)


class AbsUrlNode(defaulttags.URLNode):
    def render(self, context):
        """Returns the complete url."""
        return get_absolute_uri(super().render(context), request=context.get("request"))

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse prefix node and return a Node.
        """
        url = defaulttags.url(parser, token)
        return cls(
            view_name=url.view_name, args=url.args, kwargs=url.kwargs, asvar=url.asvar
        )


@register.tag("abs_url")
def do_abs_url(parser, token):
    return AbsUrlNode.handle_token(parser, token)


@register.simple_tag(takes_context=True)
def build_absolute_uri(context, url):
    """
    Returns the complete url.
    """
    return get_absolute_uri(url, request=context.get("request"))


@register.filter("strong")
def do_strong(value):
    return mark_safe(f"<strong>{value}</strong>")

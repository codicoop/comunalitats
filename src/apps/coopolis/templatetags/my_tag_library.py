from django import template
from django.templatetags import static
from django.conf import settings

register = template.Library()


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag('fullstatic')
def do_static(parser, token):
    return FullStaticNode.handle_token(parser, token)


@register.simple_tag
def external_static(path):
    return settings.EXTERNAL_STATIC+path

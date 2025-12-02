from django import template

register = template.Library()


@register.filter(name="conv_int")
def to_int(value):
    return int(value)

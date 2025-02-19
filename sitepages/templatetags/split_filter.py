from django import template

register = template.Library()

@register.filter(name="split")
def split(value, delimiter=","):
    """Splits a string by the given delimiter (default is comma)"""
    return value.split(delimiter) if value else []

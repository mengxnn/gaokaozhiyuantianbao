from django import template

register = template.Library()

@register.filter(name='abs')
def absolute_value(value):
    return abs(value)
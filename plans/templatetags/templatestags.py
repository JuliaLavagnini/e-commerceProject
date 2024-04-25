from django import template

register = template.Library()

@register.filter
def split_by_newline(description):
    return description.split('\n')
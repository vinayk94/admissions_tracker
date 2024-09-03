from django import template

register = template.Library()

@register.filter
def replace_spaces(value):
    return value.replace(' ', '_')

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary.get(key)
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    """Returns a value from a dictionary via a template."""
    return dictionary.get(key)
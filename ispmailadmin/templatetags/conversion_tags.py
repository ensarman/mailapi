from django import template

byte_to_gigabyte_factor = 1073741824

register = template.Library()


@register.filter
def btogb(value, toint=False):
    """Converts the value in bytes to Gigabytes

    Args:
        value (int): value in bytes
        toint (bool, optional): if the return the value will be float. Defaults to False.

    Returns:
        int, float: converted value
    """
    converted = value / byte_to_gigabyte_factor
    return int(converted) if toint else converted


@register.filter
def gbtob(value):
    return value * byte_to_gigabyte_factor
from django import template
from django.conf import settings

byte_to_gigabyte_factor = settings.BYTE_TO_GIGABYTE_FACTOR

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
    converted = value / settings.BYTE_TO_GIGABYTE_FACTOR
    return int(converted) if toint else converted


@register.filter
def mbtogb(value, toint=False):
    """Converts the value in megabytes to Gigabytes

    Args:
        value (int): value in megabytes
        toint (bool, optional): if the return the value will be float. Defaults to False.

    Returns:
        int, float: converted value
    """
    converted = value / settings.MEGABYTE_TO_GIGABYTE_FACTOR
    return int(converted) if toint else converted


@register.filter
def kbtogb(value, toint=False):
    """Converts the value in kilobytes to Gigabytes

    Args:
        value (int): value in megabytes
        toint (bool, optional): if the return the value will be float. Defaults to False.

    Returns:
        int, float: converted value
    """
    converted = value / settings.KILOBYTE_TO_GIGABYTE_FACTOR
    return int(converted) if toint else converted


@register.filter
def gbtob(value):
    return value * settings.BYTE_TO_GIGABYTE_FACTOR

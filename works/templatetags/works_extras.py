from django import template
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()


@register.filter(name='exclude')
def exclude(value, excluding_set):
    to_exclude = excluding_set.values('user')
    value = value.exclude(user__in=to_exclude)
    return value


@register.filter(name='get_object')
def get_object(value, obj):
    try:
        value = value.get(user=obj)
        return value
    except ObjectDoesNotExist:
        return None


@register.filter(name='object_exist')
def object_exist(value, obj):
    try:
        value = value.get(user=obj)
        return True
    except ObjectDoesNotExist:
        return False


@register.filter(name='dates')
def dates(value):
    now = timezone.now()
    if now > value:
        return True
    else:
        return False

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def is_recent(time):
    """
    Template tag for each post,
    check if the time since created_on is less than a week or not.

    Request:
    time: datetime

    Response:
    is_recent: boolean
    """
    return time + timezone.timedelta(days=7) > timezone.now()
   

# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|robohash:150 }}
@register.filter
def robohash(email, size=200):
    url = f'https://robohash.org/{email}?size={size}x{size}'
    return mark_safe(f'<img src="{url}">')

from django import template
from django.utils import timezone

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

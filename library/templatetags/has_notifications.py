from django import template
from ..models import Notification

register = template.Library()


@register.simple_tag
def has_notifications(user):
    """
    Templatetag, który sprawdza czy użytkownik
    ma nieprzeczytane powiadomienia
    """
    notifications = Notification.objects.filter(user=user, read=False)
    if len(notifications) <= 0:
        return ''
    else:
        return 'alert_notification'

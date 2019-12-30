from django.core.cache import cache

from conferences.models import Conference


def conference_name(request):
    """
    Adds the conference name to the context.
    """
    name = cache.get('conference_name')
    if not name:
        conference = Conference.objects.first()
        name = conference.name if conference else 'Unnamed'
        cache.set('conference_name', name, 600)

    return {'conference_name': name}


def polling_interval(request):
    """
    Adds the time for the client to wait until polling for unread messages to
    the context.
    """
    polling_interval = cache.get('polling_interval')
    if not polling_interval:
        conference = Conference.objects.first()
        polling_interval = conference.polling_interval if conference else 60
        cache.set('polling_interval', polling_interval, 60)

    return {'polling_interval': polling_interval}

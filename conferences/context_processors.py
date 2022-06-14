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

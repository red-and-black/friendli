from functools import wraps
from django.http import Http404


def superuser_required(view):
    """
    Decorator that restricts access to a view to superusers only.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):

        # Allow an active superuser to access the view.
        if request.user.is_superuser and request.user.is_active:
            return view(request, *args, **kwargs)

        # Raise 404 for other users
        raise Http404()

    return wrapper


def public(view):
    """
    Decorator that indicates that a view is visible to all users, including
    anonymous users.

    It's for purely semantic purposes and has no functionality.
    """
    return view

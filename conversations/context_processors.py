from conversations.models import Message


def unread_messages_count(request):
    """
    Adds the number of conversations with unread messages to the context.

    If the user is authenticated, this will be an integer greater than or equal
    to zero.

    For anonymous users, this will be None.
    """
    user = request.user
    if user.is_authenticated:
        count = Message.objects.filter(is_read=False, receiver=user).count()
    else:
        count = None

    return {'unread_messages_count': count}

from conversations.models import Conversation


def conversations_unread_count(request):
    """
    Adds the number of conversations with unread messages to the context.

    If the user is authenticated, this will be an integer greater than or equal
    to zero.

    For anonymous users, this will be None.
    """
    user = request.user

    if user.is_authenticated:
        count = Conversation.c_objects.with_unread_messages(user).count()
    else:
        count = None

    return {'conversations_unread_count': count}

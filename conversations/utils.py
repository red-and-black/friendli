from django.utils import timezone


def conversation_time(last_message_datetime):
    """
    Accepts a datetime.

    Returns a human-readable string which is either:
    * the time since that datetime if it was less than a day ago, or
    * the day if it was less than a week ago, or
    * the date if it was more than a week ago.
    """
    now = timezone.now()
    time_since_last_message = now - last_message_datetime
    seconds = time_since_last_message.total_seconds()
    last_message_datetime_with_timezone = last_message_datetime.astimezone()

    if seconds < 60:
        return 'Now'
    elif seconds < (60 * 60):
        return "%dm" % (seconds // 60)
    elif seconds < (60 * 60 * 24):
        return "%dh" % (seconds // (60 * 60))
    elif seconds < (60 * 60 * 24 * 7):
        return last_message_datetime_with_timezone.strftime('%a')
    elif seconds < (60 * 60 * 24 * 7 * 365):
        return last_message_datetime_with_timezone.strftime('%d %b')
    else:
        return last_message_datetime_with_timezone.strftime('%d %b %Y')


def message_time(message_datetime):
    """
    Accepts a datetime.

    Returns a human-readable string which is either:
    * the time since that datetime if it was less than an hour ago, or
    * the day and time if it was less than a week ago,
    * the date and time if it was more than a week ago.
    """
    now = timezone.now()
    time_since_last_message = now - message_datetime
    seconds = time_since_last_message.total_seconds()
    message_datetime_with_timezone = message_datetime.astimezone()

    if seconds < 60:
        return 'Now'
    elif seconds < (60 * 60):
        return "%dm" % (seconds // 60)
    elif seconds < (60 * 60 * 24 * 7):
        return message_datetime_with_timezone.strftime('%a %H:%M')
    elif seconds < (60 * 60 * 24 * 7 * 365):
        return message_datetime_with_timezone.strftime('%d %b, %H:%M')
    else:
        return message_datetime_with_timezone.strftime('%d %b %Y, %H:%M')

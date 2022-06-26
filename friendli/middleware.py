from logging import getLogger


class NoCachingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = (
            'no-cache="Set-Cookie, Set-Cookie2", no-store, must-revalidate'
        )
        response["Pragma"] = "no-cache"
        return response


class RequestLoggingMiddleware(object):
    """Middleware which logs every request."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = getLogger('django.all_requests')

    def process_string(self, key, obj):
        """Accepts a key and an object.

        If the object is a string longer than 100 characters, truncates it.

        If the object is a string which looks like a password or is a CSRF
        token, omits it.

        If the object is not a string, returns it unaltered.
        """
        if isinstance(obj, str):
            if ('password' in key.lower() or 'token' in key.lower()):
                return '**omitted**'
            else:
                max_string_length = 100
                string_length = len(obj)
                if string_length <= max_string_length:
                    return obj
                else:
                    return '%s...(+%s chars)' % (
                        obj[:max_string_length],
                        str(string_length - max_string_length)
                    )
        else:
            return obj

    def __call__(self, request):
        # Process the request.
        log_entry = 'User: %s -- %s -- %s' % (
            request.user.pk if request.user.pk else 'Anon',
            request.method,
            request.build_absolute_uri(),
        )

        # Append POST data if there is any.
        if request.method == 'POST':
            log_entry += ' -- '

            request_string = '{'

            # Add form data.
            for key, value in request.POST.items():
                request_string += (
                    '%s: \'%s\', ' % (key, self.process_string(key, value))
                )

            # Add files data, if there is any.
            if request.FILES:
                for key, value in request.FILES.iteritems():
                    request_string += (
                        '%s: \'%s\', ' % (key, value.name)
                    )

            request_string = '%s%s' % (request_string[0: -2], '}')

            log_entry += request_string

            self.logger.info(log_entry)

        response = self.get_response(request)

        # Do nothing with the response.

        return response

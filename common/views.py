from django.http import HttpResponse


def serve_serviceworker_file(request):
    response = HttpResponse("", content_type="application/javascript")
    response["Content-Disposition"] = 'inline; filename="sw.js"'
    response['Content-Length'] = 0

    return response

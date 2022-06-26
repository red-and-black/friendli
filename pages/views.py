from django.shortcuts import render

from friendli.decorators import public

from conferences.models import Conference


@public
def faqs(request):
    conference = Conference.objects.last()
    return render(request, 'faqs.html', {
        'conference': conference,
    })


@public
def landing(request):
    conference = Conference.objects.last()
    return render(request, 'landing.html', {
        'conference': conference,
    })

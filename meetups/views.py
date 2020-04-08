from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import (
    Http404,
    JsonResponse
)
from django.shortcuts import redirect, render
from django.utils import timezone

from profiles.models import Profile

from meetups.forms import MeetupForm
from meetups.models import (
    Meetup,
    StarredMeetup,
)


@login_required
def new_meetup(request):
    if request.method == 'POST':
        form = MeetupForm(request.POST)
        if form.is_valid():
            meetup = form.save(commit=False)
            meetup.organiser = request.user
            meetup.save()
            form.save_m2m()
            return redirect('meetups')
    else:
        form = MeetupForm()
    return render(request, 'new_meetup.html', {
        'form': form,
    })


@login_required
def edit_meetup(request, pk):
    meetup = Meetup.objects.get(pk=pk)
    if request.user != meetup.organiser:
        raise Http404
    if request.method == 'POST':
        form = MeetupForm(request.POST, instance=meetup)
        if form.is_valid():
            form.save()
            return redirect('meetups')
    else:
        form = MeetupForm(instance=meetup)
    return render(request, 'edit_meetup.html', {
        'form': form,
    })


@login_required
def meetups(request):
    meetups = Meetup.objects.all()
    current_meetups = []
    for meetup in meetups:
        meetup_datetime = datetime.combine(meetup.end_date, meetup.end_time)
        if meetup_datetime.astimezone() >= timezone.now():
            current_meetups.append(meetup)
    stars = StarredMeetup.objects.\
        filter(meetups_starring_profile=request.user.profile)
    starred_meetups = [star.starred_meetup for star in stars]
    return render(request, 'meetups.html', {
        'current_meetups': current_meetups,
        'starred_meetups': starred_meetups,
    })


@login_required
def past_meetups(request):
    meetups = Meetup.objects.all()
    stars = StarredMeetup.objects.\
        filter(meetups_starring_profile=request.user.profile)
    starred_meetups = [star.starred_meetup for star in stars]
    past_meetups = []
    for meetup in meetups:
        meetup_datetime = datetime.combine(meetup.end_date, meetup.end_time)
        if meetup_datetime.astimezone() < timezone.now():
            past_meetups.append(meetup)
    return render(request, 'past_meetups.html', {
        'past_meetups': past_meetups,
        'starred_meetups': starred_meetups,
    })


@login_required
def my_meetups(request):
    my_meetups = Meetup.objects.filter(organiser=request.user)

    return render(request, 'my_meetups.html', {
        'my_meetups': my_meetups,
    })


@login_required
def starred_meetups(request):
    stars = StarredMeetup.objects.\
        filter(meetups_starring_profile=request.user.profile)
    starred_meetups = [star.starred_meetup for star in stars]
    return render(request, 'starred_meetups.html', {
        'starred_meetups': starred_meetups,
    })


@login_required
def meetup_star(request, pk):
    profile = Profile.objects.get(user=request.user)
    starred_meetup = Meetup.objects.get(pk=pk)
    starred_meetups = Meetup.objects.filter(starred=request.user.profile)
    if starred_meetup in starred_meetups:
        starred_meetup.starred.remove(profile)
        action = 'unstarred'
    else:
        starred_meetup.starred.add(profile)
        action = 'starred'

    response = {'meetup': starred_meetup.pk, 'action': action}
    return JsonResponse(response)

from django.shortcuts import redirect, render

from meetups.forms import MeetupForm
from meetups.models import Meetup


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


def edit_meetup(request, pk):
    meetup = Meetup.objects.get(pk=pk)
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


def meetups(request):
    meetups = Meetup.objects.all()

    return render(request, 'meetups.html', {
        'meetups': meetups,
    })

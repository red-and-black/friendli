from django.db import models

from profiles.models import (
    PersonalInterest,
    ProfessionalInterest,
)


class Meetup(models.Model):
    name = models.CharField(max_length=50)
    organiser = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
    personal_interests = models.ManyToManyField(PersonalInterest, blank=True)
    prof_interests = models.ManyToManyField(ProfessionalInterest, blank=True)
    starred = models.ManyToManyField(
        'profiles.Profile',
        through='StarredMeetup',
        related_name='starring_profile'
    )

    class Meta:
        ordering = ['start_date', 'start_time']


class StarredMeetup(models.Model):
    meetups_starring_profile = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='as_meetups_starrer',
    )
    starred_meetup = models.ForeignKey(
        'meetups.Meetup',
        on_delete=models.CASCADE,
        related_name='starred_meetup',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

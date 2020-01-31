from django.db import models

from profiles.models import (
    PersonalInterest,
    ProfessionalInterest,
)


class Meetup(models.Model):
    name = models.CharField(max_length=50)
    organiser = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
    personal_interests = models.ManyToManyField(PersonalInterest, blank=True)
    prof_interests = models.ManyToManyField(ProfessionalInterest, blank=True)

    class Meta:
        ordering = ['date', 'time']

from django.db import models


class Conference(models.Model):
    name = models.CharField(max_length=255)
    hashtag = models.CharField(max_length=40)
    collective_noun = models.CharField(max_length=40, default='attendees')
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    link = models.URLField(blank=True)
    coc_link = models.URLField(blank=True)
    message = models.TextField(max_length=500, blank=True)

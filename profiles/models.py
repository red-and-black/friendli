from django.db import models


class ProfessionalInterest(models.Model):
    prof_interest = models.CharField(max_length=255)

    def __str__(self):
        return self.prof_interest

    class Meta:
        ordering = ['prof_interest']


class PersonalInterest(models.Model):
    personal_interest = models.CharField(max_length=255)

    def __str__(self):
        return self.personal_interest

    class Meta:
        ordering = ['personal_interest']


class Language(models.Model):
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language

    class Meta:
        ordering = ['language']


class LookingFor(models.Model):
    looking_for = models.CharField(max_length=255)

    def __str__(self):
        return self.looking_for

    class Meta:
        ordering = ['looking_for']


class Profile(models.Model):
    user = models.OneToOneField(
        'auth.User',
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    personal_interests = models.ManyToManyField(PersonalInterest, blank=True)
    prof_interests = models.ManyToManyField(ProfessionalInterest, blank=True)
    detail = models.TextField(max_length=2000, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    looking_for = models.ManyToManyField(LookingFor, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    github = models.CharField(max_length=255, blank=True)
    ask_me = models.TextField(max_length=500, blank=True)
    teach_me = models.TextField(max_length=500, blank=True)

    starred = models.ManyToManyField(
        'auth.User',
        through='Starred',
        related_name='starring_profile'
    )
    blocked = models.ManyToManyField(
        'auth.User',
        through='Blocked',
        related_name='blocking_profile'
    )
    unread_message_counter = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return 'Profile for %s' % self.user.get_username()

    class Meta:
        ordering = ['-pk']


class Blocked(models.Model):
    # TODO: Improve related_names
    blocking_profile = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='as_blocker',
    )
    blocked_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='blocked_profiles',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Starred(models.Model):
    # TODO: Improve related_names
    starring_profile = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='as_starrer',
    )
    starred_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='starred_profiles',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

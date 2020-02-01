from django import forms

from .models import Meetup


class MeetupForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(),
        input_formats=['%d/%m/%y', '%d/%m/%Y'],
    )
    time = forms.TimeField(
        widget=forms.TimeInput(),
        input_formats=['%I:%M %p', '%H:%M', '%H:%M:%S', '%I %p'],
    )

    class Meta:
        model = Meetup
        fields = (
            'name',
            'date',
            'time',
            'location',
            'details',
            'prof_interests',
            'personal_interests'
        )

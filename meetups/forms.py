from django import forms

from .models import Meetup


class MeetupForm(forms.ModelForm):

    class Meta:
        model = Meetup
        fields = (
            'name',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'location',
            'details',
            'prof_interests',
            'personal_interests'
        )

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            start_date = cleaned_data.get("start_date")
            end_date = cleaned_data.get("end_date")
            start_time = cleaned_data.get("start_time")
            end_time = cleaned_data.get("end_time")

            if start_date == end_date and start_time > end_time:
                error_msg = "The end time must be later than the start time."
                self.add_error('end_time', error_msg)
            elif start_date > end_date:
                error_msg = "The end date must be on or after the start date."
                self.add_error('end_date', error_msg)

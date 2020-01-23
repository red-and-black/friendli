
from django import forms
from .models import Conference


class ConferenceForm(forms.ModelForm):
    """
    A form to add, remove or edit a Conference
    """
    start_date = forms.DateField(
        widget=forms.DateInput(),
        input_formats=['%d/%m/%y'],
    )

    end_date = forms.DateField(
        widget=forms.DateInput(),
        input_formats=['%d/%m/%y'],
    )

    class Meta:
        model = Conference
        fields = (
            'name',
            'hashtag',
            'collective_noun',
            'location',
            'start_date',
            'end_date',
            'link',
            'coc_link',
            'message',
            'polling_interval'
        )

from django import forms

from behaviour.models import BehaviourReport


class BehaviourReportForm(forms.ModelForm):
    class Meta:
        model = BehaviourReport
        fields = ('report',)


class UpdateBehaviourReportForm(forms.ModelForm):
    class Meta:
        model = BehaviourReport
        fields = ('status', 'public_outcome', 'private_outcome')

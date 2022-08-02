from django import forms
from polls.models import PollModel


class CreatePollForm(forms.ModelForm):
    class Meta:
        model = PollModel
        exclude = ("createdBy",)
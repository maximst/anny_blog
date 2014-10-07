from django import forms
from models import PollVoice


class PollVoiceForm(forms.ModelForm):
    class Meta:
        model = PollVoice

    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll', None)
        super(PollVoiceForm, self).__init__(*args, **kwargs)

        if poll is not None:
            choices = poll.choices.values_list('id', 'choice')
            self.fields['pollchoice'].widget = forms.RadioSelect(choices=choices)

from django import forms
from models import PollVoice


class PollVoiceForm(forms.ModelForm):
    poll = None

    class Meta:
        model = PollVoice
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll', None)
        super(PollVoiceForm, self).__init__(*args, **kwargs)

        if self.poll is not None:
            choices = self.poll.choices.values_list('id', 'choice')
            self.fields['pollchoice'].widget = forms.RadioSelect(choices=choices)

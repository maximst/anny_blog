from django import forms
from models import PollChoice, PollVoice


class PollVoiceForm(forms.ModelForm):
    model = PollVoice

    def __init__(self, *args, **kwargs):
        super(PollVoiceForm, self).__init__(*args, **kwargs)
        poll_id = kwargs.get('poll_id')
        if poll_id is not None:
            self.fields['pollchoice'].queryset = PollChoice.objects\
                                            .filter(poll_id=poll_id)


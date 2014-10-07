from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    user = models.ForeignKey(User)
    question = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)

    def __unicode__(self):
        return self.question

    @property
    def voices(self):
        return PollVoice.objects.filter(pollchoice__poll_id=self.id)

    @property
    def choices(self):
        return PollChoice.objects.filter(poll=self)

    def get_voices_dict(self, user=None):
        voices = self.voices.values('pollchoice')\
            .annotate(voices=models.Count('pollchoice')).values('pollchoice_id',
                                                        'pollchoice__choice',
                                                        'voices')
        sum_count = sum(v['voices'] for v in voices)
        user_choice_ids = self.voices.filter(user=user)\
                                    .values_list('pollchoice_id', flat=True)
        for i, value in enumerate(voices):
            voices[i]['is_self_voice'] = False
            if value['pollchoice_id'] in user_choice_ids:
                voices[i]['is_self_voice'] = True

            percent = round((100.0 / sum_count) * value['voices'], 2)
            voices[i]['percent'] = percent
            voices[i]['int_percent'] = percent.__int__()

        return voices


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('poll', 'choice')

    def __unicode__(self):
        poll = self.poll.question
        poll = poll.endswith('?') and poll or u'%s?' % poll
        return u'%s %s!' % (poll, self.choice)


class PollVoice(models.Model):
    user = models.ForeignKey(User)
    pollchoice = models.ForeignKey(PollChoice)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pollchoice')

    def __unicode__(self):
        return u'User %s voice: %s' % (self.user, self.pollchoice)

    @property
    def poll(self):
        return self.pollchoice.poll

    @property
    def choice(self):
        return self.pollchoice.choice

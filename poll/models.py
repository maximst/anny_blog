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
        return PollChoice.objects.filter(poll=self).order_by('order')

    def get_voices_dict(self, user=None):
        voices_list = []
        choices = self.choices
        voices = dict(self.voices.values('pollchoice').annotate(voices=models.Count('pollchoice'))\
                                                        .values_list('pollchoice_id', 'voices'))
        sum_count = sum(voices.values())
        user_choice_ids = self.voices.filter(user=user).values_list('pollchoice_id', flat=True)

        for choice in choices:
            voices_count = voices.get(choice.id, 0)
            percent = round((100.0 / sum_count) * voices_count, 2)
            voice = {
                'choice': choice.choice,
                'voices': voices_count,
                'percent': percent,
                'int_percent': percent.__int__(),
                'is_self_voice': False
            }

            if choice.id in user_choice_ids:
                voice['is_self_voice'] = True

            voices_list.append(voice)

        return voices_list


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

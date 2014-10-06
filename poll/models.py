from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    user = models.ForeignKey(User)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)

    def __unicode__(self):
        return self.question

    @property
    def voices(self):
        return PollVoice.objects.filter(pollchoice__poll_id=self.id)


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        poll = self.poll.question
        poll = poll.endswith('?') and poll or u'%s?' % poll
        return u'%s %s!' % (poll, self.choice)


class PollVoice(models.Model):
    user = models.ForeignKey(User)
    pollchoice = models.ForeignKey(PollChoice)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'User %s voice: %s' % (self.user, self.pollchoice)

    @property
    def poll(self):
        return self.pollchoice.poll

    @property
    def choice(self):
        return self.pollchoice.choice

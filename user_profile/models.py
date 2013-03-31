#-*-coding: utf8-*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


from social_auth.models import UserSocialAuth

from pytz import all_timezones

class UserProfile(models.Model):
    SEX_CHOICES = (
        (0, 'Неопределен'),
        (1, 'Женский'),
        (2, 'Мужской')
    )

    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True,
                                default='avatars/default.png')
    signature = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    timezone = models.CharField(max_length=32, default='Europe/Kiev',
                                  choices=zip(all_timezones, all_timezones))
    sex = models.PositiveSmallIntegerField(default=0, choices=SEX_CHOICES)
    bdate = models.DateField(auto_now=False, auto_now_add=False,
                                                    null=True, blank=True)

    def __unicode__(self):
        if self.user.get_full_name():
            return u'%s (%s)' % (self.user.get_full_name(), self.user.username)
        else:
            return u'%s' % self.user.username

    def sex_name(self):
        return u'%s' % self.SEX_CHOICES[self.sex]

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User, dispatch_uid='user_profile.UserProfile')
def user_post_save(sender, **kwargs):
    """ Create user profile """
    user = kwargs.get('instance', None)
    # raw is used when loaddata is running
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        try:
            uprof = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            uprof = UserProfile(user=user)
            uprof.save()

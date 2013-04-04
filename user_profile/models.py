#-*-coding: utf8-*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings

from social_auth.models import UserSocialAuth

from pytz import all_timezones
from datetime import date

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
        return dict(self.SEX_CHOICES)[self.sex]

    def year_old(self):
        tdate = date.today()
        if not self.bdate or not self.bdate.year:
            return 0

        full_year_old = tdate.year - self.bdate.year
        if self.bdate.month < tdate.month and self.bdate.day < tdate.month:
            return full_year_old - 1
        else:
            return full_year_old

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


@receiver(pre_save, sender=User, dispatch_uid='user_profile.UserProfile')
def user_pre_save(sender, **kwargs):
    new_user = kwargs.get('instance', None)
    old_user = sender.objects.get(id=new_user.id)
    if new_user.is_active != old_user.is_active:
        if new_user.is_active:
            msg = EmailMessage(
                u'Учетная запись %s активирована' % new_user.username,
                (u'<html>'
                u'<meta http-equiv="Content-Type" content="text/html; '
                u'charset=UTF-8"><body>'
                u'Ваша учетная запись активирована<br />'
                u'Теперь вы можете '
                u'<a href="http://%s/accounts/login/">войти</a> '
                u'</body></html>') % settings.HOSTNAME,
                u'admin@%s' % settings.HOSTNAME,
                [new_user.email]
            )
            msg.content_subtype = "html"
            msg.send()
        else:
            admins = sender.objects.filter(is_superuser=True)
            msg = EmailMessage(
                u'Учетная запись %s заблокирована' % new_user.username,
                (u'<html>'
                u'<meta http-equiv="Content-Type" content="text/html; '
                u'charset=UTF-8"><body>'
                u'Ваша учетная запись заблокирована :-('
                u'</body></html>'),
                u'admin@%s' % settings.HOSTNAME,
                [new_user.email]
            )
            msg.content_subtype = "html"
            msg.send()


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

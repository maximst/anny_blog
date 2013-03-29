from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from social_auth.models import UserSocialAuth

from pytz import all_timezones
from urllib2 import urlopen

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True,
                                default='avatars/default.png')
    signature = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    timezone = models.CharField(max_length=32, default='Europe/Kiev',
                                  choices=zip(all_timezones, all_timezones))

    def __unicode__(self):
        if self.user.get_full_name():
            return u'%s (%s)' % (self.user.get_full_name(), self.user.username)
        else:
            return u'%s' % self.user.username

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

@receiver(post_save, sender=UserSocialAuth,
          dispatch_uid='social_auth.models.UserSocialAuth')
def user_sa_post_save(sender, **kwargs):
    usa = kwargs.get('instance', None)
    # raw is used when loaddata is running
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        uprof = UserProfile.objects.get(user__pk=usa.user_id)

        if usa.provider == 'facebook':
            facebook_api = 'http://graph.facebook.com/%s/picture' %\
                                                 str(usa.uid)
            image_url = urlopen(facebook_api).url
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            # TODO: Convert image to PNG
            img_filename = '%i.png' % usa.user_id
            uprof.avatar.save(img_filename, File(img_temp))
            uprof.save()

        if usa.provider == 'vkontakte-oauth2':
            vk_api = vkontakte.API(token=usa.extra_data['access_token'])
            result = vk_api.users.get(fields='sex,bdate,photo_100,country,city',
                                                                  uids=usa.uid)
            image_url = result[0]['photo_100']
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            # TODO: Convert image to PNG
            img_filename = '%i.png' % usa.user_id
            uprof.avatar.save(img_filename, File(img_temp))
            uprof.save()



from django.contrib.auth import login
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from urllib2 import urlopen
import vkontakte

def set_user_profile(backend, details, response, social_user, uid, \
      user, *args, **kwargs):
    if user:
        uprof = user.profile
        usa = social_user
        if usa.provider == 'facebook':
            facebook_api = 'http://graph.facebook.com/%s/picture?type=large' %\
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

    login(kwargs['request'], user)


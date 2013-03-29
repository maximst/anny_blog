from django.contrib.auth import login
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from urllib2 import urlopen
import vkontakte
from StringIO import StringIO
from PIL import Image

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

            img = Image.open(img_temp)
            if img.mode != 'RGB':
              img = img.convert('RGB')
            min_side = min(img.size)
            max_side = max(img.size)
            offsets = [0, 0]
            size = [min_side, min_side]
            offsets[img.size.index(max_side)] = (max_side - min_side) / 2
            size[img.size.index(max_side)] = min_side + max(offsets)
            img = img.crop((offsets[0], offsets[1], size[0], size[1]))
            img = img.resize(settings.AVATAR_SIZE, Image.ANTIALIAS)
            f = StringIO()
            img.save(f, 'PNG')

            img_filename = '%i.png' % usa.user_id
            uprof.avatar.save(img_filename, File(f))
            uprof.save()

        if usa.provider == 'vkontakte-oauth2':
            vk_api = vkontakte.API(token=usa.extra_data['access_token'])
            result = vk_api.users.get(fields='sex,bdate,photo_100,country,city',
                                                                  uids=usa.uid)
            image_url = result[0]['photo_100']
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()

            img = Image.open(img_temp)
            if img.mode != 'RGB':
              img = img.convert('RGB')
            f = StringIO()
            img.save(f, 'PNG')

            img_filename = '%i.png' % usa.user_id
            uprof.avatar.save(img_filename, File(f))
            uprof.sex = result[0]['sex']
            uprof.save()

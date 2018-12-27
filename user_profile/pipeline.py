from django.contrib.auth import login
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.cache import cache

from urllib2 import urlopen
import vk
from StringIO import StringIO
from PIL import Image
from datetime import date
from pyfaceb import FBGraph


def set_user_profile(backend, details, response, social, uid, \
      user, *args, **kwargs):

    if user:
        uprof = user.profile
        usa = social
        if usa.provider == 'facebook':
            GENDER = {
                'male': 2,
                'female': 1
            }

            facebook_api = 'http://graph.facebook.com/%s/picture?type=large' %\
                                                 str(usa.uid)
            image_url = urlopen(facebook_api).url
            img_temp = StringIO(urlopen(image_url).read())

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
            fb = FBGraph(usa.extra_data['access_token'])
            me = fb.get('me')
            uprof.sex = GENDER.get(me['gender'], 0)
            bdate = me['birthday'].split('/')
            bdate = map(int, bdate)
            uprof.bdate = date(bdate[2], bdate[0], bdate[1])
            uprof.save()

        if usa.provider == 'vk-oauth2':
            vk_api = vk.API(token=usa.extra_data['access_token'])
            result = vk_api.users.get(fields='sex,bdate,photo_100,country,city',
                                                                  uids=usa.uid)
            image_url = result[0]['photo_100']
            img_temp = StringIO(urlopen(image_url).read())
            img_temp.flush()

            img = Image.open(img_temp)
            if img.mode != 'RGB':
              img = img.convert('RGB')
            f = StringIO()
            img.save(f, 'PNG')

            img_filename = '%i.png' % usa.user_id
            uprof.avatar.save(img_filename, File(f))
            uprof.sex = result[0]['sex']
            bdate = result[0]['bdate'].split('.')
            bdate.reverse()
            if len(bdate) == 2:
                bdate.insert(0, '0')
            uprof.bdate = date(*map(int, bdate))
            uprof.save()

    cache.clear()

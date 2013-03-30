#-*-coding: utf8-*-
from django import forms
from django.conf import settings
from django.core.files import File

from models import UserProfile

from pytz import all_timezones
from PIL import Image
from StringIO import StringIO


class ProfileForm(forms.Form):
    avatar = forms.ImageField(required=False, label='Аватар')
    signature = forms.CharField(max_length=255, widget=forms.Textarea,
                                        required=False, label='Подпись')
    location = forms.CharField(max_length=255, required=False, label='Откуда')
    timezone = forms.CharField(max_length=32, initial='Europe/Kiev',
                              label='Временная зона',
            widget=forms.Select(choices=zip(all_timezones, all_timezones)))
    sex = forms.IntegerField(label='Пол',
                      widget=forms.Select(choices=UserProfile.SEX_CHOICES))
    bdate = forms.DateField(required=False, label='Дата рождения')
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')
    email = forms.EmailField(required=False)
    delete_avatar = forms.BooleanField(required=False, label='Удалить')

    def save(self, user=None, avatar=None):
        profile = user.profile
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile.bdate = self.cleaned_data['bdate']
        profile.sex = self.cleaned_data['sex']
        profile.location = self.cleaned_data['location']
        profile.timezone = self.cleaned_data['timezone']
        profile.signature = self.cleaned_data['signature']

        if avatar:
            if avatar.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(u'Размер изображения превышает %i\
                  Мб.' % (settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024*1024)))

            img_temp = StringIO(avatar.read())

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

            img_filename = '%i.png' % user.pk

            if profile.avatar.name != profile.avatar.field.default:
                profile.avatar.storage.delete(profile.avatar.name)
            profile.avatar.save(img_filename, File(f))
        elif self.cleaned_data['delete_avatar']:
            if profile.avatar.name != profile.avatar.field.default:
                profile.avatar.storage.delete(profile.avatar.name)
                profile.avatar.name = profile.avatar.field.default
        profile.save()
        user.save()

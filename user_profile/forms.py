#-*-coding: utf8-*-
from django import forms

from models import UserProfile

from pytz import all_timezones


class ProfileForm(forms.Form):
    avatar = forms.ImageField()
    signature = forms.CharField(max_length=255, widget=forms.Textarea)
    location = forms.CharField(max_length=255)
    timezone = forms.CharField(max_length=32, initial='Europe/Kiev',
            widget=forms.Select(choices=zip(all_timezones, all_timezones)))
    sex = forms.IntegerField(widget=forms.Select(
                                          choices=UserProfile.SEX_CHOICES))
    bdate = forms.DateField()

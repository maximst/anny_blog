# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import UserProfile
from forms import ProfileForm


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        pass
    else:
        form = ProfileForm(user.profile.__dict__)

    return render(request, 'registration/profile.html', {'form': form})


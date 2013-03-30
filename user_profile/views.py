# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from models import UserProfile
from forms import ProfileForm


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            avatar = request.FILES.get('avatar')
            form.save(user, avatar)
            return redirect(reverse('profile'))
    else:
        user_dict = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        user_dict.update(user.profile.__dict__)
        form = ProfileForm(user_dict)

    return render(request, 'registration/profile.html', {'form': form})


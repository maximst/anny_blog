#-*-coding: utf8-*-
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as django_logout
from django.utils import simplejson as json

from voting.models import Vote


def homepage(request):
    model = ContentType.objects.get(app_label='content',
                                    model=settings.DISPLAY_CONTENT_TYPES[0])
    return None

def logout(request):
    redirect_url = request.META.get('HTTP_REFERER')
    if not redirect_url or reverse('login') in redirect_url:
        redirect_url = '/'
    django_logout(request)
    return redirect(redirect_url)

def profile(request):
    return redirect('/')

@login_required
def vote(request, app, model, pk, vote):
    redirect_url = request.META.get('HTTP_REFERER')
    user = request.user

    try:
        content_type = ContentType.objects.get(app_label=app, model=model)
    except ContentType.DoesNotExist:
        raise Http404()

    try:
        content_model = content_type.model_class()
        obj = content_model.objects.get(pk=pk)
    except content_model.DoesNotExist:
        raise Http404()

    Vote.objects.record_vote(obj, user, int(vote))

    if not redirect_url or reverse('login') in redirect_url:
        try:
            redirect_url = reverse(model, kwargs={'slug': obj.slug})
        except:
            redirect_url = '/'
    if request.is_ajax():
        score = Vote.objects.get_score(obj)
        user_vote = Vote.objects.get_for_user(obj, request.user)
        if user_vote:
            user_vote = 0
        else:
            user_vote = 1
        score.update({'user_vote': user_vote})
        return HttpResponse(json.dumps(score), mimetype="application/json")
    else:
        return redirect(redirect_url)

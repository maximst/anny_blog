#-*-coding: utf8-*-
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as django_logout
from django.utils import simplejson as json
from django.core.mail import EmailMessage
from django.forms import ValidationError

from voting.models import Vote
from forms import RegistrationForm


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

def registration(request):
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user_pk = form.save(request.FILES.get('avatar'))
                admins = User.objects.filter(is_superuser=True)
                msg = EmailMessage(
                    u'Новый пользователь %s' % request.POST['username'],
                    (u'Зарегистрировался новый пользователь '
                    u'<a href="http://%s/admin/auth/user/%i">%s</a>'
                    u'<br />'
                    u'Данные:<br /><ul>%s</ul>') % (settings.HOSTNAME, user_pk,
                                          request.POST['username'], form.as_ul()),
                    u'admin@%s' % settings.HOSTNAME,
                    [a.email for a in admins]
                )
                msg.content_subtype = "html"
                msg.send()
                return redirect(reverse('registration-thanks'))
            except ValidationError:
                pass
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})

def registration_thanks(request):
    return render(request, 'registration/registration_thanks.html')

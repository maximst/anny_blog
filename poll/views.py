# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from .forms import PollVoiceForm
from .models import Poll


@login_required
def vote(request):
    next = request.GET.get('next', request.META.get('HTTP_REFERER') or reverse('home'))
    poll = get_object_or_404(Poll, id=request.POST.get('poll_id'))
    form = PollVoiceForm(request.POST, poll=poll)

    if form.is_valid():
        pollvoice = form.save(commit=False)
        pollvoice.user_id=request.user.id
        pollvoice.save()
        cache.clear()
    return redirect(next)
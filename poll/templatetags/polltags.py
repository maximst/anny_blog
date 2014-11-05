from django import template
from poll.forms import PollVoiceForm


register = template.Library()


@register.inclusion_tag('poll/poll_form.html', takes_context=True)
def poll(context, poll):
    request = context['request']
    context.update({
        'poll': poll,
        'form': None,
        'voices': None,
    })

    poll_voices = poll.voices.filter(pollchoice__poll=poll, user=request.user)

    if poll_voices.exists():
        context['voices'] = poll.get_voices_dict(request.user)
    else:
        form = PollVoiceForm(poll=poll)
        context['form'] = form

    return context

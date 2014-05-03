import vkontakte
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.decorators import ajax_navigation

from forms import SearchForm

def get_vk_audio(vk_api, query=None):
    users = vk_api.users.get()

    if query is not None:
        audio_list = vk_api.audio.search(q=query,
                                        auto_complete=1,
                                        search_own=1,
                                        count=1000)
        audio_list = audio_list[1:]
    else:
        audio_list = vk_api.audio.get()


    audio_list.sort(key=lambda a: (-int(a['owner_id'] == int(users[0]['uid'])),
                                   a['artist'], a['title']))

    result = []
    prev_audio = None
    for audio in audio_list:
        audio['is_self'] = audio['owner_id'] == int(users[0]['uid'])
        if prev_audio is not None and audio['is_self'] != prev_audio['is_self']:
            audio['breakline'] = True
        result.append(audio)
        prev_audio = audio

    return result

@ajax_navigation
def vksearch(request):
    user = request.user

    context = {
        'show_login': False,
        'redirect_querystring': 'next=%s' % reverse('vksearch')
    }

    if not user.is_authenticated():
        context['show_login'] = True
        return render(request, 'vksearch/vksearch.html', context)

    try:
        usa = user.social_auth.get()
    except user.social_auth.model.DoesNotExist:
        context['show_login'] = True
        return render(request, 'vksearch/vksearch.html', context)
    else:
        vk_api = vkontakte.API(token=usa.extra_data['access_token'])

    if request.GET:
        form = SearchForm(request.GET)
    else:
        form = SearchForm()
    context['form'] = form

    query = None
    if form.is_valid():
        query = form.cleaned_data['query']

    try:
        audio_list = get_vk_audio(vk_api, query=query)
    except vkontakte.VKError:
        context['show_login'] = True
        return render(request, 'vksearch/vksearch.html', context)

    if not audio_list:
        return render(request, 'vksearch/vksearch.htm', context)
    paginator = Paginator(audio_list, 50)

    page = request.GET.get('p')
    try:
        audio_list = paginator.page(page)
    except PageNotAnInteger:
        audio_list = paginator.page(1)
    except EmptyPage:
        audio_list = paginator.page(paginator.num_pages)

    context['content'] = audio_list


    return render(request, 'vksearch/vksearch.html', context)

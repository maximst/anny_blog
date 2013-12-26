#!-*-coding: utf8-*-
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.paginator import Page
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog

from voting.models import Vote

import urllib2

register = template.Library()

@register.filter
def plus(value, arg):
    if (type(value) in (int, float) and type(arg) in (int, float)) \
        or (arg.isdigit() and value.isdigit()):
        return int(value) + int(arg)
    return value

@register.filter
def diff(value, arg):
    if (type(value) in (int, float) and type(arg) in (int, float)) \
        or (arg.isdigit() and value.isdigit()):
        return int(value) - int(arg)
    return value

@register.inclusion_tag('menubar.html', takes_context=True)
def menubar(context):
    sections = []
    for slug, title in settings.MENU_ITEMS:
        try:
            url = reverse(slug+'-list')
        except:
            url = '#'
        sections.append({'slug': slug, 'title': title, 'url': url})

    current_section = context['request'].META['PATH_INFO'].split('/')[1]
    context.update({'current_section': current_section, 'sections': sections,
                                                'admin': settings.ADMINS[0]})
    return context

@register.inclusion_tag('breadcrump.html', takes_context=True)
def breadcrump(context):
    crumps = context['request'].META['PATH_INFO'].split('/')[:-1]

    urls = map(lambda c: crumps[:crumps.index(c)+1], crumps)
    urls[0].append(u'')

    titles = ['home'] + crumps[1:]

    crumps = zip(urls, titles)
    return {'crumps': crumps}

@register.inclusion_tag('vote.html', takes_context=True)
def vote(context):
    if not isinstance(context['content'], Page):
        ct = ContentType.objects.get_for_model(context['content'].__class__)
    score = Vote.objects.get_score(context['content'])
    user_vote = Vote.objects.get_for_user(context['content'],
                                          context['request'].user)
    if user_vote:
        user_vote = 0
    else:
        user_vote = 1
    return {'app': ct.app_label, 'model': ct.model, 'pk': context['content'].pk,
      'user_vote': user_vote, 'score': score, 'user': context['request'].user}

@register.inclusion_tag('vote.html', takes_context=True)
def vote_list(context, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    score = Vote.objects.get_score(blog)
    user_vote = Vote.objects.get_for_user(blog,
                                          context['request'].user)
    if user_vote:
        user_vote = 0
    else:
        user_vote = 1
    return {'app': 'blog', 'model': 'blog', 'pk': blog.pk,
      'user_vote': user_vote, 'score': score, 'user': context['request'].user}

@register.simple_tag(takes_context=True)
def meta(context, t, *args):
    try:
        content = context.get('content')[0]
        detail = False
    except:
        content = context.get('content')
        detail = True

    if not content or not isinstance(content, Blog):
        detail = False

    if t == 'title':
        if detail:
            res = content.title
        else:
            res = 'Anny'
    elif t == 'description':
        if detail:
            res = content.body
        else:
            res = 'Шик по последней моде! Следи за модой!'
    elif t == 'image':
        if detail:
            res = ''
        else:
            image = u'http://%s%simg/logo.png' % (settings.HOSTNAME,
                                                  settings.STATIC_URL)
            res = ('<meta content="%s" property="og:image">\n'
              '     <link rel="image_src" href="%s" />') % (image, image)
    elif t == 'keywords':
        if detail:
            keywords = content.tags.all()
            keywords = [t.name for t in keywords]
            res = ', '.join(keywords)
            if keywords:
                res += ', '
        else:
            res = ''
    else:
        res = ''

    return res

@register.simple_tag
def get_settings():
    return settings

@register.simple_tag(takes_context=True)
def setlinks(context):
    request = context['request']
    url = 'http://%s%s' % (request.META['HTTP_HOST'], request.META['PATH_INFO'])
    setlinks_url = 'http://show.setlinks.ru/page.php?host=follow-chic.com&start=1&count=20&p=6d6e10342d591fd102032427afb42eca&uri=%s' % url
    result = urllib2.urlopen(setlinks_url)

    if result.code == 200:
        return result.read()
    return None

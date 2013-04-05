#!-*-coding: utf8-*-
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.paginator import Page
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog

from voting.models import Vote

register = template.Library()

@register.filter
def diff(value, arg):
    return int(value) - arg

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
        title = 'Anny'
        description = 'Шик по последней моде! Следи за модой!'
        image = u'http://%s%simg/logo.png' % (settings.HOSTNAME,
                                             settings.STATIC_URL)
        keywords = []
    except:
        content = context.get('content')
        if content:
            title = content.title
            description = content.body
            image = False
            keywords = content.tags.all()
            keywords = [for t.name in keywords]
        else:
            title = 'Anny'
            description = 'Шик по последней моде! Следи за модой!'
            image = u'http://%s%simg/logo.png' % (settings.HOSTNAME,
                                             settings.STATIC_URL)
            keywords = []
    if t == 'title':
        res = title
    elif t == 'description':
        res = description
    elif t == 'image':
        if image:
            res = ('<meta content="%s" property="og:image">\n'
              '     <link rel="image_src" href="%s" />') % (image, image)
        else:
            res = ''
    elif t == 'keywords':
        res = ', '.join(keywords)
        if keywords:
            res = ', ' + res

    return res

@register.simple_tag
def get_settings():
    return settings

#!-*-coding: utf8-*-
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.paginator import Page
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog

from voting.models import Vote

import zlib
import urllib
import urllib2
import sqlite3

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
            res = 'Anny Star'
    elif t == 'description':
        if detail:
            res = content.body
        else:
            res = u'Шик по последней моде! Следи за модой!'
    elif t == 'image':
        if detail:
            res = ''
        else:
            image = u'http://%s%simg/logo.png' % (settings.HOSTNAME,
                                                  settings.STATIC_URL)
            res = (u'<meta content="%s" property="og:image">\n'
              u'     <link rel="image_src" href="%s" />') % (image, image)
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
def links(context):
    request = context.get('request')
    if request:
        url = request.META.get('PATH_INFO', '')
        url_list = url.split('://')
        if len(url_list) > 1:
            url = '://'.join(url_list[1:])

        if url.startswith('/'):
            url = u'follow-chic.com%s' % url

        query_string = request.META.get('QUERY_STRING')
        if query_string:
            url += '?%s' % query_string
    else:
        url = u'follow-chic.com/'

    if url.endswith('/'):
        alt_url = url[:-1]
    else:
        alt_url = '{}/'.format(url)

    quoted_url = urllib.quote(url.encode('utf-8'))
    alt_quoted_url = urllib.quote(alt_url.encode('utf-8'))

    conn = sqlite3.connect(settings.LINKS_DB)
    sql = conn.cursor()

    links = []
    for provider in ['mainlink', 'linkfeed']:
        try:
            res = sql.execute('SELECT * FROM {} WHERE url = ? OR url = ? OR url = ? OR url = ?'.format(provider), (url, alt_url, quoted_url, alt_quoted_url))

            for link in res:
                links.append(u'<li>%s</li>' % link[2])
        except Exception:
            pass

    return u'<ul class="linx cached">%s</ul>' % '\n'.join(links)


@register.simple_tag(takes_context=True)
def setlinks(context):
    request = context['request']
    full_url = request.build_absolute_uri()
    crc_uri_1 = str(zlib.crc32(full_url[8:]) % (1<<32))
    crc_uri_2 = str(zlib.crc32(full_url) % (1<<32))
    qs = urllib.urlencode({
        '1': '1',
        'host': 'follow-chic.com',
        'p': '6d6e10342d591fd102032427afb42eca',
    })
    setlinks_url = 'http://show.setlinks.ru/?%s' % qs

    def _filter(row):
        row_list = row.split()
        return row_list and row_list[0] in (crc_uri_1, crc_uri_2) or False

    try:
        result = urllib2.urlopen(setlinks_url, timeout=3)
        result = result.code == 200 and result.readlines() or None
    except:
        return '<!--6d6e1-->'
    else:
        res = result and filter(_filter, result) or None
        return res and res[0].decode('cp1251').replace(res[0].split()[0], '<!--6d6e1-->') or '<!--6d6e1-->'

    url = request.META.get('PATH_INFO', '')
    url_withouth_slash = url.endswith('/') and url[:-1] or url
    query_string = request.META.get('QUERY_STRING')
    if query_string:
        url += '?%s' % query_string
        url_withouth_slash += '?%s' % query_string

    setlinks_querystring = urllib.urlencode({
        'host': 'follow-chic.com',
        'start': '1',
        'count': '20',
        'p': '6d6e10342d591fd102032427afb42eca',
        'uri': url.encode('utf-8'),
    })

    setlinks_querystring_withouth_slash = urllib.urlencode({
        'host': 'follow-chic.com',
        'start': '1', 
        'count': '20',   
        'p': '6d6e10342d591fd102032427afb42eca',
        'uri': url_withouth_slash.encode('utf-8'),
    })

    setlinks_url = 'http://show.setlinks.ru/page.php?%s' % setlinks_querystring
    setlinks_url_withouth_slash = 'http://show.setlinks.ru/page.php?%s' % setlinks_querystring_withouth_slash

    try:
        result = urllib2.urlopen(setlinks_url, timeout=3)
        result = result.code == 200 and result.read() or None
        if not result:
            result = urllib2.urlopen(setlinks_url_url_withouth_slash, timeout=3)
            result = result.code == 200 and result.read() or None
    except:
        return None
    else:
        return result

    return None


@register.filter
def ext_media(url):
    url = url.replace(u'/media/', u'/follow-chic/media/blog/')
    return u'https://{}{}'.format(settings.EXT_MEDIA_IP, url)

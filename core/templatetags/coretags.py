#!-*-coding: utf8-*-
from django import template
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Page
from django.utils import html
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog

from voting.models import Vote

import zlib
import urllib
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

    urls = list(map(lambda c: crumps[:crumps.index(c)+1], crumps))
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

    quoted_url = urllib.parse.quote(url.encode('utf-8'))
    alt_quoted_url = urllib.parse.quote(alt_url.encode('utf-8'))

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
    return html.format_html('<ul class="linx unstyled cached">{}</ul>', html.mark_safe('\n'.join(links)))


@register.simple_tag(takes_context=True)
def setlinks(context):
    request = context.get('request')
    if not request:
        return ''

    full_url = request.build_absolute_uri()
    crc_uri_1 = str(zlib.crc32(full_url[full_url.startswith('https') and 8 or 7:].encode())).encode()
    crc_uri_2 = str(zlib.crc32(full_url.encode())).encode()

    qs = urllib.parse.urlencode({
        'host': 'follow-chic.com',
        'p': '6d6e10342d591fd102032427afb42eca',
        'k': 'utf-8'
    })
    setlinks_url = 'http://show.setlinks.ru/?%s' % qs

    def _filter(row):
        row_list = row.split()
        return row_list and row_list[0] in (crc_uri_1, crc_uri_2) or False

    try:
        result = urllib.request.urlopen(setlinks_url, timeout=3)
        result = result.code == 200 and result.readlines() or None
    except:
        return ''
    else:
        res = result and list(filter(_filter, result)) or None
        return res and html.mark_safe(res[0].replace(res[0].split()[0], b'<!--6d6e1-->').decode()) or ''


@register.filter
def ext_media(url):
    if settings.DEBUG:
        return url

    url = url.replace(u'/media/', u'/follow-chic/media/blog/')
    return u'https://{}{}'.format(settings.EXT_MEDIA_IP, url)

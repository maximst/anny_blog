# -*-coding: utf8-*-
import random
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.db.models import F

from models import Blog, Comment, Article, InstagramBlog
from forms import CommentForm

from tag.models import ArticleTag
from core.models import Log
from core.decorators import ajax_navigation
from poll.forms import PollVoiceForm


def log_write(request):
    user_agent = request.META.get('HTTP_USER_AGENT')
    if user_agent is not None and 'YandexMetrika' in user_agent:
        return None
    log_row = Log(
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1'),
        port = int(request.META.get('REMOTE_PORT', '0')),
        method = request.META.get('REQUEST_METHOD', 'GET'),
        path = request.path,
        query_get = request.GET.__str__(),
        query_post = request.POST.__str__(),
        sessionid = request.COOKIES.get('sessionid', ''),
        http_referer = request.META.get('HTTP_REFERER', ''),
        http_user_agent = user_agent,
    )
    if request.user.is_authenticated():
        log_row.user = request.user

    log_row.save()


@cache_page(settings.CACHE_TIMEOUT)
def instagram_detail(request, category, slug):
    instagram_blog = get_object_or_404(InstagramBlog, category__slug=category, slug=slug)

    InstagramBlog.objects.filter(id=instagram_blog.id).update(
        views_count=F('views_count') + random.randint(1, 3)
    )

    return render(request, 'blog/instagram.html', {'content': instagram_blog})


@cache_page(settings.CACHE_TIMEOUT)
def instagram_list(request, category):
    content = InstagramBlog.objects.select_related('category').filter(category__slug=category).order_by('-create_time')
    if content:
        paginator = Paginator(content, 16)

        page = request.GET.get('p')
        try:
            content = paginator.page(page)
        except PageNotAnInteger:
            content = paginator.page(1)
        except EmptyPage:
            content = paginator.page(paginator.num_pages)

    return render(request, 'blog/instagram_list.html', {'content': content})


@ajax_navigation
@cache_page(settings.CACHE_TIMEOUT)
def article_list(request):
    contents = Article.objects.all().order_by('-create_time')
    if not contents:
        return render(request, 'blog/blog_list.html', {'content': contents})
    paginator = Paginator(contents, 10)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_list.html', {'content': content})



@ajax_navigation
@cache_page(settings.CACHE_TIMEOUT)
def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blog/article.html', {'content': article})


@ajax_navigation
@cache_page(settings.CACHE_TIMEOUT)
def blog_detail(request, slug):
#    try:
#        log_write(request)
#    except:
#        pass
    user = request.user

    content = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=content)
    context = {'content': content, 'comments': comments}
    context.update(csrf(request))

    if request.method == 'POST' and user.is_authenticated():
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            ip = request.META['REMOTE_ADDR']
            comment_form.save(content, user, ip)
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
    context['comment_form'] = comment_form

    Blog.objects.filter(id=content.id).update(
        views_count=F('views_count') + random.randint(1, 3)
    )

    return render(request, 'blog/blog_detail.html', context)


@ajax_navigation
@cache_page(settings.CACHE_TIMEOUT)
def blog_list(request):
    #log_write(request)
    contents = Blog.objects.language('all').all().order_by('-create_time')
    if not contents:
        return render(request, 'blog/blog_list.html', {'content': contents})
    paginator = Paginator(contents, 16)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    last_date = content[0].create_time.date()
    for c in content:
        content[content.index(c) - 1].__setattr__('linebreack',
                            (c.create_time.date() != last_date))
        if c.create_time.date() != last_date:
            content[content.index(c) - 1].__setattr__('post_date', last_date)
        last_date = c.create_time.date()
    content[-1].__setattr__('post_date', last_date)
    content[-1].__setattr__('linebreack', True)
    return render(request, 'blog/blog_list.html', {'content': content})


@ajax_navigation
@cache_page(settings.CACHE_TIMEOUT)
def tags(request, tag=None):
    #log_write(request)
    if tag:
        blogs = Blog.objects.filter(tags__slug__in=[tag], deleted=False).order_by('-create_time')
        insts = InstagramBlog.objects.select_related('category').filter(
            tags__slug__in=[tag],
            deleted=False,
            category__enabled=True
        ).order_by('-create_time')

        contents = sorted(chain(blogs, insts), key=lambda o: o.create_time, reverse=True)
    else:
        contents = ArticleTag.objects.all()
        return render(request, 'tag_list.html', {'content': contents})

    if not contents:
        return render(request, 'blog/blog_list.html', {'content': contents})
    paginator = Paginator(contents, 16)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    last_date = content[0].create_time.date()
    for c in content:
        content[content.index(c) - 1].__setattr__('linebreack',
                            (c.create_time.date() != last_date))
        if c.create_time.date() != last_date:
            content[content.index(c) - 1].__setattr__('post_date', last_date)
        last_date = c.create_time.date()
    content[-1].__setattr__('post_date', last_date)
    content[-1].__setattr__('linebreack', True)
    return render(request, 'blog/blog_list.html', {'content': content})

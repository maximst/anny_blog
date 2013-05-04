# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Blog, Comment
from forms import CommentForm

from tag.models import ArticleTag
from core.models import Log

def log_write(request):
    log_row = Log(
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1'),
        port = int(request.META.get('REMOTE_PORT', '0')),
        method = request.META.get('REQUEST_METHOD', 'GET'),
        path = request.path,
        query_get = request.GET.__str__(),
        query_post = request.POST.__str__(),
        sessionid = request.COOKIES.get('sessionid', ''),
        http_referer = request.META.get('HTTP_REFERER', ''),
        http_user_agent = request.META.get('HTTP_USER_AGENT', ''),
        user = request.user
    )
    log_row.save()

def blog_detail(request, slug):
    log_write(request)
    user = request.user

    content = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=content)
    contents = {'content': content, 'comments': comments}
    contents.update(csrf(request))

    if request.method == 'POST' and user.is_authenticated():
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            ip = request.META['REMOTE_ADDR']
            comment_form.save(content, user, ip)
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
    contents['comment_form'] = comment_form

    return render(request, 'blog/blog_detail.html', contents)


def blog_list(request):
    log_write(request)
    contents = Blog.objects.all().order_by('-create_time')
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


def tags(request, tag=None):
    log_write(request)
    if tag:
        contents = Blog.objects.filter(tags__name__in=[tag])\
                                    .order_by('-create_time')
    else:
        contents = ArticleTag.objects.all()
        return render(request, 'tag_list.html', {'content': contents})

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
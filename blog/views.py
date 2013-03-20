# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Blog, Comment

def blog_detail(request, slug):
    content = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=content)
    contents = {'content': content, 'comments': comments}
    contents.update(csrf(request))
    return render(request, 'blog/blog_detail.html', contents)


def blog_list(request):
    contents = Blog.objects.all().order_by('-create_time')
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
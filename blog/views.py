# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Blog

def blog_detail(request, slug):
    content = get_object_or_404(Blog, slug=slug)
    contents = {'content': content}
    contents.update(csrf(request))
    return render(request, 'blog/blog_detail.html', contents)


def blog_list(request):
    contents = Blog.objects.all()
    paginator = Paginator(contents, 15)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'blog/blog_list.html', {'content': content})
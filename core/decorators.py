#!-*-coding: utf8-*-
from django.http import JsonResponse
from django.core.cache import cache

from bs4 import BeautifulSoup


def ajax_navigation(fn):
    def wrapper(request, *args, **kwargs):
      if not request.is_ajax():
          return fn(request, *args, **kwargs)

      cache_key = u'ajax_{}'.format(request.META['PATH_INFO'])
      if request.META.get('QUERY_STRING'):
          cache_key += u'?{}'.format(request.META['QUERY_STRING'])

      cached_content = cache.get(cache_key)
      if cached_content:
          return JsonResponse(cached_content)

      old_response = fn(request, *args, **kwargs)

      soup = BeautifulSoup(old_response.content)
      content = soup.find('div', {'id': 'container'})
      title = soup.find('title')
      description = soup.find('meta', {'name': 'description'})
      keywords = soup.find('meta', {'name': 'keywords'})
      image = soup.find('link', {'rel': 'image_src'})

      response = {
          'content': content.__str__()[20:-6],
          'title': title.text,
          'keywords': dict(keywords.attrs)['content']
      }

      if description is None:
          response['description'] = u'Шик по последней моде! Следи за модой!'
      else:
          response['description'] = dict(description.attrs)['content']

      if image is None:
          response['image'] = ''
      else:
          response['image'] = dict(image.attrs)['href']

      if not cached_content:
          cache.set(cache_key, response)

      return JsonResponse(response)
    return wrapper

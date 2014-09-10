#!-*-coding: utf8-*-
from django.utils import simplejson as json
from django.http import HttpResponse
from django.core.cache import cache

from BeautifulSoup import BeautifulSoup


def ajax_navigation(fn):
    def wrapper(request, *args, **kwargs):
      if not request.is_ajax():
          return fn(request, *args, **kwargs)

      cache_key = 'ajax_%s' % request.META['PATH_INFO']
      cached_content = cache.get(cache_key)
      if cached_content:
          print 'Response from cache: ', cache_key
          return HttpResponse(json.dumps(cached_content),
                              mimetype="application/json")

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
          response['description'] = 'Шик по последней моде! Следи за модой!'
      else:
          response['description'] = dict(description.attrs)['content']

      if image is None:
          response['image'] = ''
      else:
          response['image'] = dict(image.attrs)['href']

      if not cached_content:
          print 'Set cache: ', cache_key
          cache.set(cache_key, response)

      return HttpResponse(json.dumps(response), mimetype="application/json")
    return wrapper
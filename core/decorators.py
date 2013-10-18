#!-*-coding: utf8-*-
from django.utils import simplejson as json
from django.http import HttpResponse

from BeautifulSoup import BeautifulSoup


def ajax_navigation(fn):
    def wrapper(request, *args, **kwargs):
      if not request.is_ajax():
          return fn(request, *args, **kwargs)

      response = fn(request, *args, **kwargs)

      soup = BeautifulSoup(response.content)
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

      return HttpResponse(json.dumps(response), mimetype="application/json")
    return wrapper
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
      #TODO: Add title, description, keywords and image
      response = {
          'content': content.__str__(),
          'title': 'Anny',
          'description': '',
          'keywords': '',
          'image': '',
      }

      return HttpResponse(json.dumps(response), mimetype="application/json")
    return wrapper
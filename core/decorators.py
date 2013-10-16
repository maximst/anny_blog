from django.utils import simplejson as json
from django.http import HttpResponse

from BeautifulSoup import BeautifulSoup


def ajax_navigation(fn):
    def wrapper(*args, **kwargs):
      if not args[0].is_ajax():
          return fn(*args, **kwargs)

      response = fn(*args, **kwargs)
      soup = BeautifulSoup(response.content)
      content = soup.find('div', {'id': 'container', 'class': 'container'})
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
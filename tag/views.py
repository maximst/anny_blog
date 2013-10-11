from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from models import ArticleTag

from time import time

@login_required
def tags_autocomplite(request):
    t = time()
    query = request.GET.get('query')

    if not request.is_ajax() or query is None:
        return HttpResponse(status=400)

    tags = ArticleTag.objects.filter(name__icontains=query)

    response = {
        'query': query,
        'suggestions': [tag.name for tag in tags],
    }

    response['query_time'] = time() - t,

    return HttpResponse(json.dumps(response), mimetype="application/json")
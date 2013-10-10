from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from models import ArticleTag

@login_required
def tags_autocomplite(request):
    query = request.GET.get('tags')

    if not request.is_ajax() or query is None:
        return HttpResponse(status=400)

    tags = ArticleTag.objects.filter(name__iendswith=query)
    
    response = {
        'query': query,
        'suggestions': [tag.name for tag in tags],
    }
    
    return HttpResponse(json.dumps(response), mimetype="application/json")
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .models import ArticleTag

from time import time

@login_required
def tags_autocomplite(request):
    t = time()
    query = request.GET.get('query')

    if not request.is_ajax() or query is None:
        return JsonResponse({'error': 'Only AJAX supported'}, status=400)

    if not request.user.is_superuser:
        return JsonResponse({'error': 'Only superuser can use this view'}, status=403)

    tags = ArticleTag.objects.filter(name__icontains=query)

    response = {
        'query': query,
        'suggestions': [tag.name for tag in tags],
    }

    response['query_time'] = time() - t,

    return JsonResponse(response)

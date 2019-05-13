from django.template.context_processors import request
from blog.models import InstagramCategory

def core(request):
    query_string = request.META['QUERY_STRING']
    query_dict = query_string.split('&')
    query_string = '&'.join(p for p in query_dict if p and not p.startswith('p='))

    categories = InstagramCategory.objects.filter(enabled=True)
    return {'querystring' : query_string, 'categories': categories}

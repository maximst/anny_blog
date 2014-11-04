from django.core.context_processors import request

def core(request):
    query_string = request.META['QUERY_STRING']
    query_dict = query_string.split('&')
    query_string = '&'.join(p for p in query_dict if p and not p.startswith('p='))
    return {'querystring' : query_string}
from django.contrib import admin
from models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'port', 'method', 'http_user_agent', 'path',
                    'http_referer', 'sessionid', 'query_get', 'query_post')
    search_fields = ('user', 'ip', 'http_user_agent', 'path',
                     'http_referer', 'sessionid', 'query_get', 'query_post')
    list_filter = ('method', 'user')


admin.site.register(Log, LogAdmin)

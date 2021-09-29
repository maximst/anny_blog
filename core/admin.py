from django.contrib import admin
from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('access_time', 'user', 'ip', 'port', 'method', 'http_user_agent', 'path',
                    'http_referer', 'sessionid', 'query_get', 'query_post')
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'ip', 'http_user_agent', 'path', 'http_referer',
                     'sessionid', 'query_get', 'query_post')
    list_filter = ('access_time', 'method', 'user')


admin.site.register(Log, LogAdmin)

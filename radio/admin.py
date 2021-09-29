from django.contrib import admin
from .models import Audio


class AudioAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'created_at', 'aid', 'player')

admin.site.register(Audio, AudioAdmin)

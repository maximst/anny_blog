from django.contrib import admin
from models import Poll, PollChoice, PollVoice


class PollChoiceInline(admin.TabularInline):
    list_display = ('poll', 'choice', 'order')
    model = PollChoice
    extra = 0


class PollAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'created_at', 'anonymous')
    inlines = (PollChoiceInline,)


class PollVoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice')


admin.site.register(Poll, PollAdmin)
admin.site.register(PollVoice, PollVoiceAdmin)

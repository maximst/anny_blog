from django.contrib import admin
from models import Blog, Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'front_page',
                                                    'on_top', 'deleted')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)

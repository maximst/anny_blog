from django.contrib import admin
from models import Blog, Comment, BlogImage


class BlogImageInline(admin.TabularInline):
  model = BlogImage
  extra = 0


class BlogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'front_page',
                                                    'on_top', 'deleted')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (BlogImageInline,)
    
    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [static_url + 'js/jquery.autocomplete.js', static_url + 'js/tag-autocomplete.js']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)

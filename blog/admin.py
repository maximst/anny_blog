from django.contrib import admin
from filer.admin.fileadmin import FileAdmin as BaseFileAdmin
from models import Blog, Comment, BlogImage, MediaFile, Article
from django.core.cache import cache


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).save_model(*args, **kwargs)

    def save_related(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).save_related(*args, **kwargs)

    def delete_model(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).delete_model(*args, **kwargs)


class BlogImageInline(admin.TabularInline):
  model = BlogImage
  extra = 0


class BlogAdmin(BaseModelAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'front_page',
                                                    'on_top', 'deleted')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (BlogImageInline,)

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [
            static_url + 'js/jquery.autocomplete.js',
            static_url + 'js/tag-autocomplite.js',
            #static_url + 'js/jquery.js'
        ]

        css = {
            'all': (static_url + 'css/tag-autocomplite.css',)
        }


class ArticleAdmin(BaseModelAdmin):
    list_display = ('__unicode__', 'user', 'create_time', 'deleted')
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [  
            static_url + 'js/jquery.autocomplete.js',
            static_url + 'js/tag-autocomplite.js',
            #static_url + 'js/jquery.js'
        ]

        css = {
            'all': (static_url + 'css/tag-autocomplite.css',)
        }



class CommentAdmin(BaseModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')


class FileAdmin(BaseFileAdmin):
    list_display = ('label', 'file')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MediaFile, FileAdmin)
admin.site.register(Article, ArticleAdmin)


from django.contrib import admin
from filer.admin.fileadmin import FileAdmin as BaseFileAdmin
from .models import (
    Blog, Comment, BlogImage, MediaFile, Article, InstagramBlog, InstagramImage,
    InstagramChannel, InstagramCategory
)
from hvad.admin import TranslatableAdmin
from django.core.cache import cache
from django.db import transaction


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).save_model(*args, **kwargs)

    def save_related(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).save_related(*args, **kwargs)
#        try:
#            with transaction.atomic():
#                return super(BaseModelAdmin, self).save_related(*args, **kwargs)
#        except Exception:
#            pass

    def delete_model(self, *args, **kwargs):
        cache.clear()
        return super(BaseModelAdmin, self).delete_model(*args, **kwargs)


class BlogImageInline(admin.TabularInline):
  model = BlogImage
  extra = 0


class BlogAdmin(TranslatableAdmin, BaseModelAdmin):
    #list_display = ('__unicode__', 'user', 'create_time', 'front_page',
    #                                                'on_top', 'deleted')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (BlogImageInline,)

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [
            static_url + 'js/jquery.autocomplete.js',
            static_url + 'js/tag-autocomplite.js',
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
        ]

        css = {
            'all': (static_url + 'css/tag-autocomplite.css',)
        }



class CommentAdmin(BaseModelAdmin):
    list_display = ('__unicode__', 'create_time', 'ip')


class FileAdmin(BaseFileAdmin):
    list_display = ('label', 'file')


class InstagramCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'enabled',)
    prepopulated_fields = {'slug': ('title',)}


class InstagramImageInline(admin.TabularInline):
  model = InstagramImage
  extra = 0


class InstagramBlogAdmin(BaseModelAdmin):
    list_display = ('__unicode__', 'create_time', 'deleted', 'category_', 'images_count', 'videos_count')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (InstagramImageInline,)
    list_filter = ('channel__channel', 'category__title', 'deleted',)
    ordering = ('-create_time',)
    search_fields = ('inst_id', 'short_code', 'inst_user', 'title',)

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [
            static_url + 'js/jquery.autocomplete.js',
            static_url + 'js/tag-autocomplite.js',
        ]

        css = {
            'all': (static_url + 'css/tag-autocomplite.css',)
        }

    def category_(self, obj):
        return obj.category.title

    def images_count(self, obj):
        return obj.images.count()

    def videos_count(self, obj):
        return obj.videos.count()


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MediaFile, FileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(InstagramBlog, InstagramBlogAdmin)
admin.site.register(InstagramChannel, admin.ModelAdmin)
admin.site.register(InstagramCategory, InstagramCategoryAdmin)

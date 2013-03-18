from django.contrib import admin
from models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'create_time', 
                                   'front_page', 'on_top', 'deleted')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)

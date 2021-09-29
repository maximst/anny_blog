from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.views import LoginView

from blog.views import (
    blog_list, blog_detail, tags, article, article_list, instagram_detail,
    instagram_list
)
from core.views import vote, logout, registration, registration_thanks, laminat
from tag.views import tags_autocomplite
from user_profile.views import profile
from vksearch.views import vksearch
from poll.views import vote as poll_vote

from django.contrib.sitemaps.views import sitemap
from sitemap import (
    BlogSitemap, CommentSitemap, BlogImageSitemap, ArticleTagSitemap,
    InstagramBlogSitemap, InstagramImageSitemap, ArticleSitemap
)

sitemaps = {
    'blog': BlogSitemap,
    'comment': CommentSitemap,
    'blog_image': BlogImageSitemap,
    'tags': ArticleTagSitemap,
    'categories': InstagramBlogSitemap,
    'categories_image': InstagramImageSitemap,
    'article': ArticleSitemap
}


admin.autodiscover()

urlpatterns = [
    url(r'^blog/(?P<slug>[\w\-]+)/$', blog_detail, name='blog'),
    url(r'^category/(?P<category>[\w\-]+)/(?P<slug>[\w\-]+)/$', instagram_detail, name='instagram'),
    url(r'^category/(?P<category>[\w\-]+)/$', instagram_list, name='instagram-list'),
    url(r'^category/', TemplateView.as_view(template_name='blog/categories.html'), name='instagram-categories'),
    url(r'^article/(?P<slug>[\w\-]+)/$', article, name='article'),
    url(r'^article/$', article_list, name='article-list'),
    url(r'^blog/$', blog_list, name='blog-list'),
    url(r'^$', blog_list, name='home'),
    url(r'^grappelli/', include(('grappelli.urls', 'grappelli'))),
    url(r'^admin/doc/', include(('django.contrib.admindocs.urls', 'admindocs'))),
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include(('django_comments_xtd.urls', 'django_comments_xtd'))),
    url(r'^vote/(?P<app>[\w\-\_]+)/(?P<model>[\w\_]+)/(?P<pk>\d+)/(?P<vote>([01]))/$', vote, name='vote'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^accounts/registration/$', registration, name='registration'),
    url(r'^accounts/registration_thanks/$', registration_thanks,
                                            name='registration-thanks'),
    url(r'^tag/(?P<tag>.+)/$', tags, name='tags'),
    url(r'^tag_autocomplite/$', tags_autocomplite, name='tags_autocomplite'),
    url(r'^tag/$', tags, name='tags'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                        name='django.contrib.sitemaps.views.sitemap'),
    path(r'captcha/', include('captcha.urls')),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^laminat/$', laminat, name='laminat'),
    url(r'^accounts/login-error/$', TemplateView.as_view(template_name="login-error.html")),
    url(r'^vksearch/$', vksearch, name='vksearch'),
    url(r'^poll-vote/$', poll_vote, name='poll-vote'),
    path(r'', include(('social.apps.django_app.urls', 'social'), namespace='social')),
    url(r'^filer/', include(('filer.urls', 'filer'))),
]

if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve,
                          {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),)

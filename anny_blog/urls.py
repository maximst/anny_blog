from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib import auth

from blog.views import blog_list, blog_detail, tags
from core.views import vote, logout, registration, registration_thanks
from user_profile.views import profile

from sitemap import BlogSitemap

sitemaps = {'blog': BlogSitemap}


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blog/(?P<slug>[\w\-]+)/$', blog_detail, name='blog'),
    url(r'^blog/$', blog_list, name='blog-list'),
    url(r'^$', blog_list, name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/$', include('django.contrib.comments.urls')),
    url(r'^vote/(?P<app>[\w\-\_]+)/(?P<model>[\w\_]+)/(?P<pk>\d+)/(?P<vote>([01]))/$', vote, name='vote'),
    url(r'^accounts/login/$', auth.views.login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/profile/$', profile, name='profile'),
    url(r'^accounts/registration/$', registration, name='registration'),
    url(r'^accounts/registration_thanks/$', registration_thanks,
                                            name='registration-thanks'),
    url(r'^accounts/social/', include('social_auth.urls')),
    url(r'^tag/(?P<tag>.+)/$', tags, name='tags'),
    url(r'^tag/$', tags, name='tags'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                                            {'sitemaps': sitemaps})
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

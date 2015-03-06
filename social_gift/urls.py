from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import  post

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'social_gift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^basicview/', include('post.urls')),
    url(r'^', include('post.urls')),
)

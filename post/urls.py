from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^page/(\d+)/$', 'post.views.pagination'),
    url(r'^sorted_members_up/$', 'post.views.sorted_members_up'),
    url(r'^sorted_members_down/$', 'post.views.sorted_members_down'),
    url(r'^sorted_days_up/$', 'post.views.sorted_days_up'),
    url(r'^sorted_days_down/$', 'post.views.sorted_days_down'),
    url(r'^sorted_gifts_up/$', 'post.views.sorted_gifts_up'),
    url(r'^sorted_gifts_down/$', 'post.views.sorted_gifts_down'),
    url(r'^search/$', 'post.views.search'),
    url(r'^find/$', 'post.views.find'),
    url(r'^for_admins/$', 'post.views.for_admins'),
    url(r'^for_admins/search_url/$', 'post.views.search_url'),
    url(r'^add_contest/$', 'post.views.add_contest'),
    url(r'^about_us/$', 'post.views.about_us'),
    url(r'^contacts/$', 'post.views.contacts'),
    url(r'^', 'post.views.posts'),
)
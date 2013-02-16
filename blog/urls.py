from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^add_blog/$', 'add_blog'),
    (r'^edit_blog/(?P<blog_id>\w+)/$', 'edit_blog'),
    (r'^delete_blog/(?P<blog_id>\w+)/$', 'delete_blog'),
    (r'^blog/(?P<slug>[\w\-]+)/$', 'blog'),
    (r'^blogs/$', 'blogs'),
    (r'^add_entry/(?P<blog_id>\w+)/$', 'add_entry'),
    (r'^edit_entry/(?P<entry_id>\w+)/$', 'edit_entry'),
    (r'^delete_entry/(?P<entry_id>\w+)/$', 'delete_entry'),
    (r'^entry/(?P<slug>[\w\-]+)/$', 'entry'),
    (r'^trnaslate_entry/(?P<entry_id>\w+)/(?P<lang>\w+)/$', 'trnaslate_entry'),
)

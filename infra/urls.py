from django.conf.urls.defaults import *

urlpatterns = patterns('infra.views',
    (r'^change_lang/(?P<lang>[\w-]+)/(?P<learn>\w+)/$', 'change_lang'),
)

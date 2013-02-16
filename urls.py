from django.conf.urls.defaults import *

from app.views import home, done, logout, error, form, form2
from app.facebook import facebook_view
from app.vkontakte import vkontakte_view
from app.odnoklassniki import ok_app, ok_app_info



handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^home/$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^vk/', vkontakte_view, name='vk_app'),
    url(r'^ok/$', ok_app , name='ok_app'),
    url(r'^ok/info/$', ok_app_info , name='ok_app_info'),
    url(r'', include('social_auth.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),   
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include('urlsadmin')),
     ('^blog/',include('blog.urls')),
     ('^$', 'blog.views.index'),
)

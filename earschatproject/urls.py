from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    url(r'^', include('chat.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
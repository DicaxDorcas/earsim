from django.conf.urls import patterns, url

from chat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^chat/(?P<user>.*)/$', views.chat),

    url(r'^send/$', views.send),
    url(r'^receive/$', views.receive),
    url(r'^sync/$', views.sync),

    url(r'^join/$', views.join),
    url(r'^leave/$', views.leave), 
)

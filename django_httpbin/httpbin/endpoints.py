from django.conf.urls import patterns
import views

urlpatterns = patterns('',
    (r'^$', views.main_page),
    (r'^/$', views.main_page),
    (r'^/ip$', views.ip),
    (r'^/user-agent$', views.user_agent),
    (r'^/headers$', views.headers),
    (r'^/get$', views.get),
)
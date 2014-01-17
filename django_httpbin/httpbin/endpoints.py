from django.conf.urls import patterns
import views

urlpatterns = patterns('',
    (r'^$', views.main_page),
    (r'^/$', views.main_page),
    (r'^/ip$', views.ip),
    (r'^/user-agent$', views.user_agent),
    (r'^/headers$', views.headers),
    (r'^/get$', views.get),
    (r'^/status/(\d+)$', views.status),
    (r'^/response-headers$', views.response_headers),
    (r'^/redirect-to$', views.redirect_to)
)
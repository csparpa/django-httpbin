from django.conf.urls import patterns, include

urlpatterns = patterns('',
    (r'^django-httpbin', include('django_httpbin.httpbin.endpoints')),
)

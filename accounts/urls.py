from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'spots/index.html'}),
)

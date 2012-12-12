from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'spots.views.index'),
    url(r'^spots/', include('spots.urls', namespace="spots")),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('registration.urls')),
)

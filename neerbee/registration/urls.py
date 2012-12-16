"""
URLConf for Django user registration and authentication.

If the default behavior of the registration views is acceptable to
you, simply use a line like this in your root URLConf to set up the
default URLs for registration::

    (r'^accounts/', include('registration.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

But if you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead. If you do, it's a
good idea to use the names ``registration_activate``,
``registration_complete`` and ``registration_register`` for the
various steps of the user-signup process.

"""


from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from neerbee.registration.views import activate, register
from neerbee.registration.forms import RegistrationFormUniqueEmail

"""
Activation keys get matched by \w+ instead of the more specific
[a-fA-F0-9]{40} because a bad activation key should still get to the view;
that way it can return a sensible "invalid key" message instead of a
confusing 404.
"""
urlpatterns = patterns('',
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        {'template': 'registration/activate.html'},
        name='registration_activate'),
    url(r'^register/$',
        register,
        {'form_class': RegistrationFormUniqueEmail,
            'template': 'registration/registration_form.html'},
        name='registration_register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)

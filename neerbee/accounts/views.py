from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from mongoengine.django.shortcuts import get_document_or_404
from mongoengine.django.auth import User

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    #UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    '''try:
        uid_int = base36_to_int(uidb36)
        user = UserModel.objects.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None'''
    print "printing: " + str(uidb36)
    try:        
        user = get_document_or_404(User, pk=uidb36)
    except (Http404):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

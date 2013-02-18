from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from functools import wraps

def already_logged_in():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            user_id = request.session.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    return HttpResponseRedirect(reverse('root_path'))
                except ObjectDoesNotExist:
                    return func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)
        return wraps(func)(inner_decorator)
    return decorator

def staff_user():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            user_id = request.session.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    if user.is_staff:
                        return func(request, *args, **kwargs)
                except ObjectDoesNotExist:
                    pass
            return HttpResponseRedirect(reverse('sessions.views.new'))
        return wraps(func)(inner_decorator)
    return decorator
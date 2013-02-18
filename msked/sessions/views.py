from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from msked.utils import add_csrf
from sessions.decorators import already_logged_in

@already_logged_in()
def new(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse('root_path'))
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('root_path'))
        else:
            messages.error(request, 'Email and/or password invalid')
    d = {
        'email': request.POST.get('email', ''),
        'next' : request.GET.get('next', ''),
        'title': 'Login',
    }
    return render_to_response('sessions/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def delete(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('sessions.views.new'))
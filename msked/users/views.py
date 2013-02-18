from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from msked.utils import add_csrf
from users.forms import UserEditForm
from users.models import Profile

@login_required
def edit(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user
    if request.user.pk != user.pk:
        return HttpResponseRedirect(reverse('users.views.edit', 
            args=[request.user.profile.slug]))
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            if password:
                user.set_password(password)
                user.save()
            user = form.save()
            if username:
                profile.slug = slugify(username)
                profile.save()
            messages.success(request, 'User updated')
            return HttpResponseRedirect(reverse('root_path'))
    form = UserEditForm(instance=user)
    d = {
        'form' : form,
        'title': 'Edit Profile',
        'user' : user,
    }
    return render_to_response('users/edit.html', add_csrf(request, d), 
        context_instance=RequestContext(request))
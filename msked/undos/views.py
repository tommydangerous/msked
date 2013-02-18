from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from msked.utils import page
from undos.models import Undo
from undos.utils import undo_action

@login_required
def list(request):
    undos = Undo.objects.all()
    d = {
        'count'  : undos.count(),
        'title'  : 'Undo History',
        'objects': undos,
    }
    return render_to_response('undos/list.html', d, 
        context_instance=RequestContext(request))

@login_required
def delete(request, pk):
    undo = get_object_or_404(Undo, pk=pk)
    undos = Undo.objects.all().order_by('-created')
    if undos and undos[0].pk == undo.pk:
        response = undo_action(undo)
        if not response:
            response = 'Seat assignment'
        messages.success(request, '%s history undone' % response)
    else:
        messages.warning(request, 'You must undo history in order')
    return HttpResponseRedirect(reverse('undos.views.list'))
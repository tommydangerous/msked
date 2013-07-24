from django.shortcuts import get_object_or_404, render

from msked.utils import add_csrf
from stations.models import Station

def detail(request, slug):
    station = get_object_or_404(Station, slug=slug)
    d = {
        'objects': station.note_set.order_by('-created'),
        'station': station,
        'title': 'Station %s' % station.name,
    }
    return render(request, 'stations/detail.html', add_csrf(request, d))
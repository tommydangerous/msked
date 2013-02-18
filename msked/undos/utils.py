from assignments.models import Assignment
from datetime import timedelta
from django.utils import timezone
from placements.models import Placement
from tasks.models import Task
from works.models import Work

def undo_action(undo):
    max_time = undo.created + timedelta(seconds=10)
    min_time = undo.created - timedelta(seconds=10)
    if undo.job:
        item = undo.job
        Task.objects.filter(job=item, created__lte=max_time, 
            created__gte=min_time).delete()
        Work.objects.filter(job=item, created__lte=max_time,
            created__gte=min_time).delete()
    elif undo.location:
        item = undo.location
        Placement.objects.filter(location=item, created__lte=max_time, 
            created__gte=min_time).delete()
    else:
        item = None
        Assignment.objects.filter(created__lte=max_time, 
            created__gte=min_time).delete()
    undo.delete()
    return item
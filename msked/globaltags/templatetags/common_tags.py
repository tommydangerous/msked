from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import re

register = template.Library()

@register.inclusion_tag('admins/user_list.html')
def admin_user_list(user):
    # render admins/user_list.html and output into templates
    # users = User.objects.all()
    pass

@register.simple_tag
def faved(reading, user):
    # If user already faved reading
    try:
        favorite = reading.favorite_set.get(user=user)
        return 'faved'
    # If user has not faved reading
    except ObjectDoesNotExist:
        return 'fave'

@register.simple_tag
def faved_title(reading, user):
    # If user already faved reading
    try:
        favorite = reading.favorite_set.get(user=user)
        return 'Unsave from favorites'
    # If user has not faved reading
    except ObjectDoesNotExist:
        return 'Save to favorites'

@register.simple_tag
def lazy_image():
    return '%simg/lazy.png' % settings.STATIC_URL

@register.filter
def make_range(n):
    """Return a list of numbers from 1 to n."""
    return range(1, n + 1)

@register.filter(is_safe=True)
def target_blank(value):
    """Add target _blank for URL link."""
    return re.sub("<a([^>]+)(?<!target=)>", '<a target="_blank"\\1>', value)

@register.filter
def time(date):
    """Return 09:15 am"""
    time  = date.strftime('%I:%M')
    am_pm = date.strftime('%p').lower()
    return '%s %s' % (time, am_pm)

@register.simple_tag
def voted(note, user):
    try:
        vote = note.vote_set.get(user=user)
        if vote.value == 1:
            return 'upVoted'
        else:
            return 'downVoted'
    except ObjectDoesNotExist:
        return 'notVoted'

@register.simple_tag
def voted_reading(reading, user):
    try:
        vote = reading.vote_set.get(user=user)
        if vote.value == 1:
            return 'upVoted'
        else:
            return 'downVoted'
    except ObjectDoesNotExist:
        return 'notVoted'
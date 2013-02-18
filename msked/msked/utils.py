from django.core.context_processors import csrf
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from msked.digg_paginator import DiggPaginator

def add_csrf(request, d):
    d.update(csrf(request))
    return d

def page(request, objects, per_page):
    """Create paginator object and return it."""
    # [leading block] [current page] [trailing block]
    # body is the size of the block that contains the currently active page
    # margin defines the minimum number of pages required between two blocks
    # tail is the number of pages in the leading and trailing blocks
    paginator = DiggPaginator(objects, per_page, body=3, margin=1, tail=2)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    return items
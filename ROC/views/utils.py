from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def item_paginator(request, item_all):
    paginator = Paginator(item_all, 20)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginar_registros(request, queryset, items_per_page=20):
    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_queryset = paginator.page(paginator.num_pages)
    
    return paginated_queryset 
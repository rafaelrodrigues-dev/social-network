from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchRank
from django.core.paginator import Paginator
from publications.models import Publication
from django.contrib.auth import get_user_model

User = get_user_model()

def search(request):
    query = request.GET.get('q', '').strip()
    results = Publication.objects.annotate(
        search=SearchVector('text', 'author__username'),
        rank=SearchRank(SearchVector('text', 'author__username'), query)
    ).filter(search=query).order_by('-rank')

    paginator = Paginator(results, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'search/pages/search_results.html',context={
        'page_obj':page_obj,
        'query': query,
        'additional_query':'&q=' + query,
        'search_type': 'posts'
    })

def search_user(request):
    query = request.GET.get('q', '').strip()
    results = User.objects.annotate(
        search=SearchVector('username', 'first_name', 'last_name'),
        rank=SearchRank(SearchVector('username', 'first_name', 'last_name'), query)
    ).filter(search=query).order_by('-rank')
    paginator = Paginator(results, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'search/pages/search_user_results.html',context={
        'page_obj':page_obj,
        'query': query,
        'additional_query':'&q=' + query,
        'search_type': 'users'
    })
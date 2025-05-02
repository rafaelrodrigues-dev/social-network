import os
from django.shortcuts import render, redirect
from publications.models import Publication,Comment
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,Http404,HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector,SearchRank

PER_PAGE = os.getenv('PER_PAGE',7)

def home(request):
    publications = Publication.objects.all().order_by('-id')
    paginator = Paginator(publications,PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'publications/pages/home.html',{
        'page_obj':page_obj,
        })

def publication_detail(request,pk):
    publication = get_object_or_404(Publication,pk=pk)
    comments = Comment.objects.filter(publication=publication,).order_by('-id')
    return render(request,'publications/pages/publication-detail.html',{
        'publication':publication,
        'comments':comments,
        'is_detail':True,
    })

def search(request):
    query = request.GET.get('q','')
    results = Publication.objects.annotate(
        search=SearchVector('text','author__username'),
        rank=SearchRank(SearchVector('text','author__username'),query)
    ).filter(search=query)
    paginator = Paginator(results,PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'publications/pages/search_results.html',context={
        'page_obj':page_obj,
        'additional_query':'&q=' + query
    })


@login_required(login_url='authors:login')
def like(request,pk):
    if request.method != 'POST':
        return JsonResponse({'error':'Invalid request'},status=400)
    publication = get_object_or_404(Publication,pk=pk)
    if publication in request.user.likes.all():
        publication.like.remove(request.user)
        liked = False
    else:
        liked = True
        publication.like.add(request.user)

    return JsonResponse({
        'liked': liked,
        'likes_count': f'{publication.like.count()}',
    })

@login_required
def comment(request,pk):
    if request.method != 'POST':
        raise Http404()
    
    publication = get_object_or_404(Publication,pk=pk)
    text = request.POST.get('text')
    author = request.user
    Comment.objects.create(
        publication=publication,
        text=text,
        author=author
    )

    return redirect(reverse('publications:publication-detail',kwargs={'pk':pk}))
    
@login_required
def delete_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.user == publication.author:
        publication.delete()
        return redirect('publications:home')
    else:
        return HttpResponseForbidden("You are not allowed to delete this publication.")
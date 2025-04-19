from django.shortcuts import render, redirect
from publications.models import Publication,Comment
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank

def home(request):
    publications = Publication.objects.all().order_by('-id')
    return render(request,'publications/pages/home.html',{
        'publications':publications
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
    query = SearchQuery(request.GET.get('q',''))
    results = Publication.objects.annotate(
        search=SearchVector('text','author__username'),
        rank=SearchRank(SearchVector('text','author__username'),query)
    ).filter(search=query)
    return render(request,'publications/pages/search_results.html',context={
        'results':results,
        'query':query
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
    
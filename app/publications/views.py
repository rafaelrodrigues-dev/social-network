import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from publications.models import Comment, Publication

PER_PAGE = os.getenv('PER_PAGE',4)

@require_POST
@login_required
def create_publication(request):
    data = request.POST
    files = request.FILES
    Publication.objects.create(text=data.get('text'),author=request.user,img=files.get('img'))
    return redirect('publications:home')

def home(request):
    publications = Publication.objects.all().order_by('-id')
    paginator = Paginator(publications,PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'publications/pages/home.html',{
        'page_obj':page_obj,
        'filter_publications': 'home'
        })

@login_required
def following_publications(request):
    publications = Publication.objects.filter(author__profile__in=request.user.profile.follow.all()).order_by('-id')
    paginator = Paginator(publications,PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'publications/pages/home.html',{
        'page_obj':page_obj,
        'filter_publications': 'following'
        })

@login_required
def publications_saved(request):
    publications = Publication.objects.filter(saved=request.user).order_by('-saved')
    paginator = Paginator(publications,PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'publications/pages/home.html',{
        'page_obj':page_obj,
        'filter_publications': 'saved'
        })

def publication_detail(request, pk):
    publication = get_object_or_404(Publication,pk=pk)
    comments_list = Comment.objects.filter(publication=publication,).order_by('-id')
    paginator = Paginator(comments_list,5)
    page_number = request.GET.get('comments_page',1)
    comments = paginator.get_page(page_number)
    return render(request,'publications/pages/publication-detail.html',{
        'publication':publication,
        'comments':comments,
    })

@require_POST
@login_required
def delete_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.user == publication.author:
        publication.delete()
        return redirect('publications:home')
    else:
        return HttpResponseForbidden("You are not allowed to delete this publication.")

@require_POST
@login_required
def like(request, pk):
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

@require_POST
@login_required
def save_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if publication in request.user.saved.all():
        publication.saved.remove(request.user)
        saved = False
    else:
        publication.saved.add(request.user)
        saved = True

    return JsonResponse({
        'saved':saved,
    })

@require_POST
@login_required
def comment(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    text = request.POST.get('text')
    author = request.user
    Comment.objects.create(
        publication=publication,
        text=text,
        author=author
    )

    return redirect(reverse('publications:publication-detail',kwargs={'pk': pk}))

@require_POST
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    publication_pk = comment.publication.pk
    if request.user == comment.author or request.user == comment.publication.author:
        comment.delete()
        return redirect(reverse('publications:publication-detail',kwargs={'pk': publication_pk}))
    else:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from publications.models import Comment, Publication
from publications.forms import PublicationForm

PER_PAGE = os.getenv('PER_PAGE',7)

class CreatePublicationView(LoginRequiredMixin, FormView):
    template_name = 'publications/pages/create_publication.html'
    form_class = PublicationForm
    success_url = reverse_lazy('publications:home')

    def form_valid(self, form):
        publication = form.save(commit=False)
        publication.author = self.request.user
        publication.save()
        return super().form_valid(form)

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
    comments_list = Comment.objects.filter(publication=publication,).order_by('-id')
    paginator = Paginator(comments_list,5)
    page_number = request.GET.get('comments_page',1)
    comments = paginator.get_page(page_number)
    return render(request,'publications/pages/publication-detail.html',{
        'publication':publication,
        'comments':comments,
        'is_detail':True,
    })

@login_required
def delete_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.user == publication.author:
        publication.delete()
        return redirect('publications:home')
    else:
        return HttpResponseForbidden("You are not allowed to delete this publication.")

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

def delete_comment(request,pk):
    if request.method != 'POST':
        raise Http404()
    
    comment = get_object_or_404(Comment,pk=pk)
    publication_pk = comment.publication.pk
    if request.user == comment.author or request.user == comment.publication.author:
        comment.delete()
        return redirect(reverse('publications:publication-detail',kwargs={'pk':publication_pk}))
    else:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
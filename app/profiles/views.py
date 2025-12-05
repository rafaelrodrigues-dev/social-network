import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from .models import Profile
from .forms import PublicationForm
from publications.models import Publication
from django.core.paginator import Paginator

PER_PAGE = os.getenv('PER_PAGE',7)

@login_required(login_url='authors:login')
def follow(request,username):
    if not request.method == 'POST':
        raise Http404()
    
    profile = get_object_or_404(Profile,user__username=username)
    
    if request.user == profile.user:
        return HttpResponse('You cannot follow yourself',status=403)
    
    if profile in request.user.profile.follow.all():
        profile.followers.remove(request.user.profile)
    else:
        profile.followers.add(request.user.profile)

    return redirect(reverse('profiles:profile',kwargs={'username':username}))
    
@login_required(login_url='authors:login')
def profile_detail(request,username):
    profile = get_object_or_404(Profile,user__username=username)
    publications = Publication.objects.filter(author__profile=profile).order_by('-id')
    paginator = Paginator(publications,PER_PAGE)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request,'profiles/profile_detail.html',context={
        'profile':profile,
        'page_obj':page_obj
    })

@login_required()
def new_publication(request,username):
    form = PublicationForm()

    return render(request,'profiles/create_publication.html',context={
        'form':form
    })

@login_required()
def new_publication_create(request,username):
    form = PublicationForm(data=request.POST,files=request.FILES)

    if form.is_valid():
        publication = form.save(commit=False)
        publication.author = request.user
        publication.save()

        return redirect(reverse('profiles:profile',kwargs={'username':username}))
    
    return redirect(reverse('profiles:new_publication',kwargs={'username':username}))

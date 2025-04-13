from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _ 
from .models import Profile
from .forms import PublicationForm
from publications.models import Publication

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

    return render(request,'profiles/profile_detail.html',context={
        'profile':profile,
        'publications':publications
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
    
    messages.error(request,_('Unable to create publication'))
    return redirect(reverse('profiles:new_publication',kwargs={'username':username}))

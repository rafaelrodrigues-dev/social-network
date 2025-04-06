from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from .models import Profile

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
    return render(request,'profiles/profile_detail.html',context={'profile':profile})

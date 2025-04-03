from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required(login_url='authors:login')
def profile_detail(request,username):
    profile = get_object_or_404(Profile,user__username=username)
    return render(request,'profiles/profile_detail.html',context={'profile':profile})

import os
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, JsonResponse
from .models import Profile
from .forms import EditProfileForm
from publications.models import Publication
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from notifications.utils import notify


class EditProfileView(LoginRequiredMixin,FormView):
    template_name = 'profiles/edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('profiles:profile',kwargs={'username':self.request.user.username})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        kwargs['user'] = self.request.user
        
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,_('Profile updated successfuly'))
        return super().form_valid(form)

@login_required()
def follow(request,username):
    if not request.method == 'POST':
        raise Http404()
    
    profile = get_object_or_404(Profile,user__username=username)
    
    if request.user == profile.user:
        return HttpResponseForbidden('You cannot follow yourself')
    
    if profile in request.user.profile.follow.all():
        profile.followers.remove(request.user.profile)
        is_following = False
    else:
        profile.followers.add(request.user.profile)
        is_following = True
        notify(
            recipient=profile.user,
            text=_('Start following you'),
            sender=request.user,
            notification_type='follow',
        )

    return JsonResponse({
        'is_following':is_following
    })

def profile_detail(request,username):
    profile = get_object_or_404(Profile,user__username=username)
    active_tab = request.GET.get('tab', 'posts')

    if active_tab == 'posts':
        publications = Publication.objects.filter(author__profile=profile).order_by('-id')
    elif active_tab == 'saved':
        publications = Publication.objects.filter(saved=profile.user).order_by('-saved')

    paginator = Paginator(publications,6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request,'profiles/profile_detail.html',context={
        'profile':profile,
        'page_obj':page_obj,
        'active_tab': active_tab
    })

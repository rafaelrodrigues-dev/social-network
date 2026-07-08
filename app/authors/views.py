from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from notifications.utils import notify

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('publications:home'))
    form_data = request.session.get('register_form_data',None)
    form = RegisterForm(form_data)
    return render(request,'authors/pages/register.html',context={
        'form':form })

@require_POST
def register_create(request):
    request.session['register_form_data'] = request.POST
    
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        authenticated_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(request,authenticated_user)

        request.session.pop('register_form_data',None)
        notify(
            recipient=request.user,
            text=_('Welcome to our platform!'),
            notification_type='system'
        )

        return redirect(reverse('profiles:profile',kwargs={'username':user.username}))
    
    return redirect(reverse('authors:register'))

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('publications:home'))
    form = LoginForm()

    return render(request,'authors/pages/login.html',context={
        'form':form,
    }
)

@require_POST
def login_create(request):

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if authenticated_user:
            login(request,authenticated_user)
            messages.success(request,_('Login successful'))

            return redirect(reverse('publications:home'))
        
        else:
            messages.error(request,_('Invalid credentials'))

    else: 
        messages.error(request,_('Invalid username or password'))

    return redirect(reverse('authors:login'))

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('authors:login'))

def about(request):
    return render(request, 'authors/pages/about.html')

def privacy_policy(request):
    return render(request, 'authors/pages/privacy.html')
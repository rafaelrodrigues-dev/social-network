from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.urls import reverse

User = get_user_model()

def register_view(request):
    form_data = request.session.get('register_form_data',None)
    form = RegisterForm(form_data)
    return render(request,'authors/pages/register.html',context={
        'form':form })

def register_create(request):
    if not request.method == 'POST':
        raise Http404()
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

        del(request.session['register_form_data'])
            
        return redirect(reverse('publications:home'))
    
    return redirect(reverse('authors:register'))

def login_view(request):
    form_data = request.session.get('login_form_data',None)
    form = LoginForm(form_data)
    return render(request,'authors/pages/login.html',context={
        'form':form,
    }
)

def login_create(request):
    if not request.method == 'POST':
        raise Http404()
    request.session['login_form_data'] = request.POST
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if authenticated_user:
            login(request,authenticated_user)
            del(request.session['login_form_data'])
            return redirect(reverse('publications:home'))
    return redirect(reverse('authors:login'))
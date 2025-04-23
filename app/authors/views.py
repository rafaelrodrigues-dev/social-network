from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm, EditAuthorForm
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()


class EditAuthorView(LoginRequiredMixin,FormView):
    template_name = 'authors/pages/edit.html'
    form_class = EditAuthorForm
    success_url = reverse_lazy('publications:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        kwargs['user'] = self.request.user
        
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,_('Profile updated syccessfuly'))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

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

        request.session.pop('register_form_data',None)

        messages.success(request,_('User registered successfully'))

        return redirect(reverse('publications:home'))
    
    return redirect(reverse('authors:register'))

def login_view(request):
    form = LoginForm()
    return render(request,'authors/pages/login.html',context={
        'form':form,
    }
)

def login_create(request):
    if not request.method == 'POST':
        raise Http404()

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

@login_required(login_url='authors:login')
def logout_view(request):
    logout(request)
    messages.success(request,_('User has been logged out'))
    return redirect('/')

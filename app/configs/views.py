from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import EditAuthorForm
from django.views.generic import FormView, TemplateView

class ConfigsView(LoginRequiredMixin, TemplateView):
    template_name = 'configs/pages/configs.html'

class EditAuthorView(LoginRequiredMixin,FormView):
    template_name = 'configs/pages/edit_author.html'
    form_class = EditAuthorForm
    success_url = reverse_lazy('publications:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        kwargs['user'] = self.request.user
        
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,_('Profile updated successfuly'))
        return super().form_valid(form)
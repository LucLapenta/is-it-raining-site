from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import logging

from .forms import CustomUserCreationForm, UserProfileForm, CustomUserChangeForm, AlertModelForm
from .models import CustomUser, Profile, Alert

logger = logging.getLogger(__name__)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class AlertListView(LoginRequiredMixin, ListView):
    template = 'alert_list.html'
    model = Alert
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        user = self.request.user
        context = Alert.objects.filter(user=user)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class CreateAlertView(LoginRequiredMixin, CreateView):
    template_name = 'users/alert_form.html'
    #model = Alert
    form_class = AlertModelForm
    success_url = reverse_lazy('alerts')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class UpdateAlertView(LoginRequiredMixin, UpdateView):
    template_name = 'users/edit_alert.html'
    model = Alert
    form_class = AlertModelForm
    success_url = '/users/alerts'
    pk_url_kwarg = 'pk'
    context_object_name = 'alert'

    def get_object(self):
        pk_ = self.kwargs.get("pk")
        return get_object_or_404(Alert, pk=pk_)

    def form_valid(self, form):
        
        print('validation')
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form) # check form HTML here
        return super().form_invalid(form)
    
class DeleteAlertView(DeleteView):

    model = Alert
    success_url = reverse_lazy('alerts')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url=self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteAlertView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('alerts')

@login_required
def view_profile(request, pk=None):
    if pk:
        user = CustomUser.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'users/profile.html', args)

@login_required
def edit_profile(request):
    #user = get_object_or_404(CustomUser, pk=pk)

    user_form = CustomUserChangeForm(
            initial={
                    'username': request.user.username,
                    'email': request.user.email
                }
        )
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Profile updated sucessfully'))
            return redirect('/users/profile')
        else:
            messages.error(request, ('invalid field'))
    else:
        
        profile_form = UserProfileForm(
            initial = {
                'phone_number': request.user.profile.phone_number,
                'zip_code': request.user.profile.zip_code,
                'cell_phone_provider': request.user.profile.cell_phone_provider
            }
        )
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


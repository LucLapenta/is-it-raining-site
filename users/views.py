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

from .forms import CustomUserCreationForm, UserProfileForm, CustomUserChangeForm
from .models import CustomUser, Profile

logger = logging.getLogger(__name__)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

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
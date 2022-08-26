from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView

from app.forms import *
from django.contrib.auth.models import User, Permission



@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            user = request.user
            user.username = username
            user.email = email
            user.save()
            return redirect(change_profile)
        else:
            user = request.user
            username = user
            email = user.email
            context = {'form': form, 'username': username, 'email': email}
            return render(request, 'settings/change_profile.html', context)
    else:
        form = ProfileForm()
        user = request.user
        username = user
        email = user.email
        context = {'form': form, 'username': username, 'email': email}
        return render(request, 'settings/change_profile.html', context)

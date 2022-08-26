from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import *
from app.services import notificationservice


@login_required
def notification_list(request):
    list = notificationservice.objects_all
    context = {'list': list}
    return render(request, 'notification/notification_list.html', context)

@login_required
def notification_change_status(request, pk, status):
    obj = notificationservice.get_object_by_pk(pk)
    if status == 'active':
        obj.access = True
    elif status == 'block':
        obj.access = False
    obj.save()
    return redirect(notification_list)

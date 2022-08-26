from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import *
from app.services import supplierservice


@login_required
def supplier_list(request):
    list = supplierservice.objects_all()
    list = list.exclude(phone=None)
    context = {'list': list}
    return render(request, 'supplier/supplier_list.html', context)

@login_required
def supplier_change_status(request, pk, status):
    obj = supplierservice.get_object_by_pk(pk)
    if status == 'active':
        obj.access = True
    elif status == 'block':
        obj.access = False
    obj.save()
    return redirect(supplier_list)

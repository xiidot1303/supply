from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import *
from app.forms import ObjectForm



@login_required
def object_list(request):
    objects = Object.objects.all()
    context = {'list': objects}
    return render(request, 'object/object_list.html', context)

class ObjectCreateView(CreateView, LoginRequiredMixin):
    form_class = ObjectForm
    template_name = 'object/object_create.html'
    success_url = '/object/list'

class ObjectEditView(UpdateView, LoginRequiredMixin):
    model = Object
    form_class = ObjectForm
    template_name = 'object/object_update.html'
    success_url = '/object/list'

@login_required
def object_delete(request, pk):
    object = Object.objects.get(pk=pk)
    object.delete()
    return redirect(object_list)



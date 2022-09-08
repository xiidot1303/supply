from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import *
from app.forms import ProductForm

@login_required
def product_list(request):
    products = Product.objects.all()
    context = {'list': products}
    return render(request, 'product/product_list.html', context)

@login_required
def product_list_by_type(request):
    products = Product.objects.all()
    context = {'list': products}
    return render(request, 'product/product_list_by_type.html', context)


class ProductCreateView(CreateView, LoginRequiredMixin):
    form_class = ProductForm
    template_name = 'product/product_create.html'
    success_url = '/product/list'

class ProductEditView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    success_url = '/product/list'

@login_required
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect(product_list)
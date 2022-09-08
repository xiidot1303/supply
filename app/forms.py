from django.forms import ModelForm, widgets, ModelMultipleChoiceField
from app.models import *
from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    email = forms.CharField(max_length=200, required=False)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = {'product_id', 'title', 'amount', 'warehouse', 'warehouse_id', 'type_id', 'type'}
        labels = {
            'product_id': 'ID',
            'title': 'Название', 
            'amount': 'Количество',
            'warehouse': 'Склад', 
            'warehouse_id': 'ID склада', 
            'type': 'Вид товара', 
            'type_id': 'ID вид товара'
        }

        widgets = {
            'product_id': forms.TextInput(attrs={"class": "form-control"}),
            'title': forms.TextInput(attrs={"class": "form-control"}), 
            'amount': forms.TextInput(attrs={"class": "form-control"}),
            'warehouse': forms.TextInput(attrs={"class": "form-control"}), 
            'warehouse_id': forms.TextInput(attrs={"class": "form-control"}), 
            'type_id': forms.TextInput(attrs={"class": "form-control"}), 
            'type': forms.TextInput(attrs={"class": "form-control"})
        }

    field_order = ['product_id', 'title', 'amount', 'warehouse', 'warehouse_id', 'type', 'type_id']

class ObjectForm(ModelForm):
    class Meta:
        model = Object
        fields = {'title'}
        labels = {
            'title': 'Название'
        }

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}), 
        }

    field_order = ['title']
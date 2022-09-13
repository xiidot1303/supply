"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from django.conf import settings
from django.conf.urls.static import static
from config import APPLICANT_BOT_API_TOKEN, SUPPLIER_BOT_API_TOKEN

from app.views.main import *
from app.views.botwebhook import *
from app.views.statement import *
from app.views.settings import *
from app.views.product import *
from app.views.supplier import *
from app.views.notification import *
from app.views.object import *

urlpatterns = [
    # main
    path('xiidot1303/', admin.site.urls),
    path('', statement_list_all, name='main'),
    path(APPLICANT_BOT_API_TOKEN, applicant_webhook),
    path(SUPPLIER_BOT_API_TOKEN, supplier_webhook),

    # auth
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile', change_profile, name = "change_profile"),

    # files
    path('files/photos/<str:file>/', get_photos),
    
    # statment
    path('statement/list/all', statement_list_all, name='statement_list_all'),
    path('statement/supplies/<int:pk>/', statement_supplies, name='statement_supplies'),
    path('statement/accept_supply/<int:pk>/', statement_accept_supply, name='statement_accept_supply'),
    path('statement/cancel/<int:pk>/', statement_cancel, name='statement_cancel'),

    # product
    path('product/list', product_list, name='product_list'),
    path('product/list_by_type', product_list_by_type, name='product_list_by_type'),
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<int:pk>/', ProductEditView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),

    # supplier
    path('supplier/list', supplier_list, name='supplier_list'),
    path('supplier/change_status/<int:pk>/<str:status>/', supplier_change_status, name='supplier_change_status'),

    # notification
    path('notification/list', notification_list, name='notification_list'),
    path('notification/change_status/<int:pk>/<str:status>/', notification_change_status, name='notification_change_status'),

    # object
    path('object/list', object_list, name='object_list'),
    path('object/create', ObjectCreateView.as_view(), name='object_create'),
    path('object/edit/<int:pk>/', ObjectEditView.as_view(), name='object_update'),
    path('object/delete/<int:pk>/', object_delete, name='object_delete'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


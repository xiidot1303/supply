from django.contrib import admin
from app.models import *

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']


class StatementAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'type', 'amount', 'status']

class SupplyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'statement', 'supplier', 'price', 'status']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'title', 'warehouse', 'amount']
    list_filter = ['title']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['group_id']

admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Statement, StatementAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Notification, NotificationAdmin)

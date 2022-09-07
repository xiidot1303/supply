from django.contrib import admin
from app.models import *

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'phone', 'lang', 'date']


class StatementAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'status']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount', 'comment']

class SupplyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'statement', 'supplier', 'price', 'status']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'title', 'warehouse', 'amount']
    list_filter = ['title']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['group_id']

class  ObjectAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Statement, StatementAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Object, ObjectAdmin)
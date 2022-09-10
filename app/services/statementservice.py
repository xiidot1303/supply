from app.models import Statement, Order
from app.services import (
    applicantservice, 
    apiservice, 
    supplierservice,
    supplyservice,
    notificationservice
    )
from django.db.models import Q

def create_and_get_object_by_update(update):
    user = applicantservice.get_object_by_user_id(update.message.chat.id)
    if filter_unfinished_objects_by_update(update):
        obj = get_current_object_by_update(update)
    else:
        obj = Statement.objects.create(user=user)
        obj = get_object_by_id(obj.pk)
        order = create_order_and_get()
        obj.orders.add(order)
    obj.save()
    return obj

def get_object_by_id(id):
    return Statement.objects.get(pk=id)

def get_current_object_by_update(update):
    obj = Statement.objects.get(status=None, user__user_id=update.message.chat.id)
    return obj

def filter_unfinished_objects_by_update(update):
    user = applicantservice.get_object_by_update(update)
    objects = Statement.objects.filter(status=None, user=user)
    return objects

def filter_active_statements_by_update(update):
    user = applicantservice.get_object_by_update(update)
    objects = Statement.objects.filter(Q(user=user) & ~Q(status='supp') & ~Q(status='cancel'))
    return objects

def create_order_and_get():
    order = Order.objects.create()
    order = Order.objects.get(pk=order.pk)
    return order

def add_order_to_the_obj(obj, order=None):
    if not order:
        order = create_order_and_get()

    obj.orders.add(order)
    obj.save()

def remove_order_from_obj(obj, order=None): # if order == None get last order of the obj
    if not order: 
        order = get_last_order_of_object(obj)
    obj.orders.remove(order)
    obj.save()
    order.delete()


def get_last_order_of_object(obj):
    order = obj.orders.all().last()
    return order

def filter_orders_of_object(obj):
    orders = obj.orders.all()
    return orders

def confirm_statement(obj=None, id=None):
    if not obj:
        obj = get_object_by_id(id)
        
    if obj.status == 'wait':
        obj.status = 'conf'
        obj.save()
        
        supplierservice.send_statement_to_suppliers(obj)
        apiservice.create_statement_api(obj)

        # notify applicant
        applicantservice.notify_user_about_statement_status(obj)
        
        return True
    else:
        return False

def cancel_statement(obj=None, id=None):
    if not obj:
        obj = get_object_by_id(id)
        
    if obj.status == 'wait':
        obj.status = 'cancel'
        obj.save()
        apiservice.cancel_statement_api(obj)
        # notify applicant
        applicantservice.notify_user_about_statement_status(obj)
        return True
    else:
        return False

def supplied_statement_by_id(obj_id):
    obj = get_object_by_id(obj_id)
    if obj.status != 'supp':
        obj.status = 'supp'
        obj.save()

        # notify groups and suppliers
        supply = supplyservice.get_confirmed_supply_of_statement(obj)
        notificationservice.send_confirmation_of_supply_to_groups(supply)
        supplierservice.send_confirmation_of_supply_to_supplier(supply)
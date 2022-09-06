from app.models import Statement, Order
from app.services import applicantservice, apiservice

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

def cancel_statement_by_id(pk):
    obj = get_object_by_id(pk)
    obj.status = 'cancel'
    obj.save()
    apiservice.cancel_statement_api(obj)

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


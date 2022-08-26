from app.models import Supply
from bots import *
from bots.strings import lang_dict
from app.services import supplierservice

def create_object(statement, supplier):
    Supply.objects.create(statement=statement, supplier = supplier)

def get_object_by_id(id):
    return Supply.objects.get(pk=id)

def get_current_object_by_update(update):
    obj = Supply.objects.get(date=None, supplier__user_id=update.message.chat.id)
    return obj

def filter_current_objects_by_update(update):
    supplier = supplierservice.get_object_by_update(update)
    objects = Supply.objects.filter(supplier=supplier, date=None)
    return objects

def filter_old_supplies_of_current_statement(update, supply):
    statement = supply.statement
    supplier = supplierservice.get_object_by_update(update)
    objects = Supply.objects.filter(statement=statement, supplier=supplier).exclude(date=None)
    return objects

def filter_supplies_by_statement(statement):
    query = Supply.objects.filter(statement=statement).exclude(status=None)
    return query

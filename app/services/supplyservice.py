from app.models import Supply
from bots import *
from bots.strings import lang_dict
from app.services import supplierservice, apiservice, applicantservice
from django.db.models import Q

def create_object(statement, supplier):
    Supply.objects.create(statement=statement, supplier = supplier)

def get_object_by_id(id):
    return Supply.objects.get(pk=id)

def get_current_object_by_update(update):
    obj = Supply.objects.get(date=None, supplier__user_id=update.message.chat.id)
    return obj

def get_confirmed_supply_of_statement(statement):
    obj = Supply.objects.get(statement=statement, status='conf')
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

def filter_supplies_for_history(supplier):
    query = Supply.objects.filter(supplier=supplier).filter(Q(status='wait') | Q(status='conf'))
    return query

def confirm_supply(supply):
    st = supply.statement
    if st.status != 'end':

        supply.status = 'conf'
        supply.save()
        st.status = 'end'
        st.supplier = supply.supplier
        st.save()
        
        # send notification to Supplier
        supplierservice.send_accepted_message_to_supplier(supply)

        # confirmation api to 1c
        apiservice.confirm_supply_api(supply)
        
        # notify applicant
        applicantservice.notify_user_about_statement_status(st, supply)

def cancel_supply(supply):
    if supply.status != 'cancel':
        supply.status = 'cancel'
        supply.save()
        supplierservice.send_cancelled_message_to_supplier(supply)
        return True
    else:
        return False

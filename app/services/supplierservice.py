from app.models import Supplier, Product
from bots import *
from bots.strings import lang_dict
from app.services import stringservice

def get_or_create(user_id):
    obj = Supplier.objects.get_or_create(user_id=user_id)
    

def get_object_by_pk(pk):
    obj = Supplier.objects.get(pk=pk)
    return obj

def get_object_by_user_id(user_id):
    obj = Supplier.objects.get(user_id=user_id)
    return obj

def get_object_by_update(update):
    obj = Supplier.objects.get(user_id=update.message.chat.id)
    return obj

def objects_all():
    return Supplier.objects.filter()

def send_statement_to_suppliers(statement):
    st = statement
    
    for s in Supplier.objects.filter(access=True).exclude(phone=None):
        text = stringservice.new_order_for_supplier(statement, supplier=s)

        # sending message
        i_apply = InlineKeyboardButton(
            text=stringservice.supply(s), 
            callback_data='supply_statement-{}'.format(st.pk)
            )
        reply_markup = InlineKeyboardMarkup([[i_apply]])
        send_newsletter(supplier_bot, s.user_id, text, reply_markup) 


def send_accepted_message_to_supplier(supply):
    supplier = supply.supplier
    text = stringservice.accepted_message_for_supplier(supply)
    send_newsletter(supplier_bot, supplier.user_id, text, pin_message=True)
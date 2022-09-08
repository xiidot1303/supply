from app.models import Notification, Product
from bots import *
from bots.strings import lang_dict
from app.services import stringservice

def create_or_edit_group(update, type):
    obj = Notification.objects.get_or_create(group_id=str(update.message.chat.id))[0]
    obj = Notification.objects.get(pk=obj.pk)
    obj.title = update.message.chat.title
    obj.type = type
    obj.save()

def objects_all():
    return Notification.objects.all()

def get_object_by_pk(pk):
    obj = Notification.objects.get(pk=pk)
    return obj

def send_statement_to_groups(statement):
    text = stringservice.new_order_for_notification(statement)

    for n in Notification.objects.filter(access=True, type='order'):
        send_newsletter(applicant_bot, n.group_id, text) 

def send_supply_to_groups(supply):
    text = stringservice.supply_details_for_notification(supply)
    
    for n in Notification.objects.filter(access=True, type='supply'):
        i_accept = InlineKeyboardButton(text='✅ Принимать', callback_data='accept_supply-{}'.format(supply.pk))
        button = InlineKeyboardMarkup([[i_accept]])
        send_newsletter(applicant_bot, n.group_id, text, reply_markup=button)
from app.models import Notification, Product
from bots import *
from bots.strings import lang_dict

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
    st = statement
    text = lang_dict['new order'][1]
    text = text.format(
        id=st.id, applicant=st.user.name, phone=st.user.phone,
    )
    text += '\n➖➖➖➖➖➖➖\n'
    
    for order in statement.orders.all():
        order_text = lang_dict['order details'][1]
        order_text = order_text.format(
            title = order.product, 
            amount = order.amount,
            product_comment = order.comment
        )
        text += order_text

        product_obj = order.product_obj
        if product_obj:
            text += '\n\n📑 В складе\n'
            text += f'Название: {product_obj.title}\nID: {product_obj.product_id}\nКоличество: {product_obj.amount}\nСклад: {product_obj.warehouse}\n\n'
        
        text += '\n➖➖➖➖➖➖➖\n'

    for n in Notification.objects.filter(access=True, type='order'):
        send_newsletter(applicant_bot, n.group_id, text) 

def send_supply_to_groups(supply):
    st = supply.statement
    products = ''
    for order in st.orders.all():
        if order.product_obj:
            continue
        order_text = lang_dict['order details'][1]
        order_text = order_text.format(
            title = order.product, 
            amount = order.amount,
            product_comment = order.comment
        )
        products += order_text + '\n\n'
        
    
    text = lang_dict['notify new supply']
    text = text.format(
        order_id=st.pk, products=products,
        supplier=supply.supplier.name, price=supply.price, due=supply.due.strftime('%d.%m.%Y'), comment=supply.comment 
    )
    for n in Notification.objects.filter(access=True, type='supply'):
        i_accept = InlineKeyboardButton(text='✅ Принимать', callback_data='accept_supply-{}'.format(supply.pk))
        button = InlineKeyboardMarkup([[i_accept]])
        send_newsletter(applicant_bot, n.group_id, text, reply_markup=button)
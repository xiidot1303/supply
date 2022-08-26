from app.models import Notification, Product
from bots import *
from bots.strings import lang_dict

def create_or_edit_group(update):
    obj = Notification.objects.get_or_create(group_id=str(update.message.chat.id))[0]
    obj = Notification.objects.get(pk=obj.pk)
    obj.title = update.message.chat.title
    obj.save()

def objects_all():
    return Notification.objects.all()

def get_object_by_pk(pk):
    obj = Notification.objects.get(pk=pk)
    return obj

def send_statement_to_groups(statement):
    st = statement
    text = lang_dict['new order'][1]
    
    product_obj = Product.objects.filter(title__icontains=statement.product)
    if product_obj:
        text += '📑 В складе\n'
    for p in product_obj:
        text += f'Название: {p.title}\nID: {p.product_id}\nКоличество: {p.amount}\nСклад: {p.warehouse}\n\n'
    
    for n in Notification.objects.filter(access=True):
        text = text.format(
            id=st.id, applicant=st.user.name, phone=st.user.phone,
            title=st.product, amount=st.amount, comment=st.comment
        )
        send_newsletter(applicant_bot, n.group_id, text) 

def send_supply_to_groups(supply):
    st = supply.statement
    text = lang_dict['notify new supply']
    for n in Notification.objects.filter(access=True):
        text = text.format(
            order_id=st.pk, title=st.product, amount=st.amount, product_comment=st.comment,
            supplier=supply.supplier.name, price=supply.price, due=supply.due.strftime('%d.%m.%Y'), comment=supply.comment 
        )
        i_accept = InlineKeyboardButton(text='✅ Принимать', callback_data='accept_supply-{}'.format(supply.pk))
        button = InlineKeyboardMarkup([[i_accept]])
        send_newsletter(applicant_bot, n.group_id, text, reply_markup=button)
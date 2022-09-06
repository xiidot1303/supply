from app.models import Supplier, Product
from bots import *
from bots.strings import lang_dict
from bots.supplier.utils import get_word

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
        text = get_word('new order', chat_id=s.user_id)
        text = text.format(
            id=st.id, applicant=st.user.name, phone=st.user.phone,
        )
        text += '\n➖➖➖➖➖➖➖\n'

        # orders text
        for order in st.orders.all():
            # dont notify if product is already available on storage
            if order.product_obj:
                continue

            order_text = get_word('order details', chat_id=s.user_id)
            order_text = order_text.format(
                title = order.product, 
                amount = order.amount,
                product_comment = order.comment
            )
            text += order_text
            text += '\n➖➖➖➖➖➖➖\n'

        # sending message
        i_apply = InlineKeyboardButton(
            text=get_word('supply', chat_id=s.user_id), 
            callback_data='supply_statement-{}'.format(st.pk)
            )
        reply_markup = InlineKeyboardMarkup([[i_apply]])
        send_newsletter(supplier_bot, s.user_id, text, reply_markup) 


def send_accepted_message_to_supplier(supply):
    supplier = supply.supplier
    st = supply.statement
    products = ''
    for order in st.orders.all():
        if order.product_obj:
            continue
        order_text = get_word('order details', chat_id=supplier.user_id)
        order_text = order_text.format(
            title = order.product, 
            amount = order.amount,
            product_comment = order.comment
        )
        products += order_text + '\n\n'
        
    text = '{}\n\n{}\n{}➖ ➖ ➖ ➖ ➖\n\n{}\n\n{}'.format(
        get_word('your supply is accepted', chat_id=supplier.user_id),
        get_word('statement details', chat_id=supplier.user_id),
        '{products}',
        get_word('applicant details', chat_id=supplier.user_id),
        get_word('supply details', chat_id=supplier.user_id),
        ).replace('\t', '')
    text = text.format(
        order_id=st.pk, products = products,
        applicant=st.user.name, phone=st.user.phone,
        supplier=supply.supplier.name, price=supply.price, 
        due=supply.due.strftime('%d.%m.%Y'), comment=supply.comment 
        )
    send_newsletter(supplier_bot, supplier.user_id, text, pin_message=True)
from bots.strings import lang_dict
from bots.applicant import utils as applicant_utils
from bots.supplier import utils as supplier_utils

def supply(supplier):
    text = supplier_utils.get_word('supply', chat_id=supplier.user_id)
    return text

def get_orders_of_statement(statement, order_text):
    st = statement
    products = ''
    for order in st.orders.all():
        if order.product_obj:
            continue
        order_text = order_text
        order_text = order_text.format(
            title = order.product, 
            amount = order.amount,
            product_comment = order.comment
        )
        products += order_text + '\n\n'
    return products

def new_order_for_notification(statement):
    st = statement
    text = lang_dict['new order'][1]
    text = text.format(
        id=st.id, applicant=st.user.name, phone=st.user.phone, object=st.object.title
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
            text += f'Название: {product_obj.title}\nID: {product_obj.product_id}\nКоличество: {product_obj.amount}\nСклад: {product_obj.warehouse}'
        
        text += '\n➖➖➖➖➖➖➖\n'
    return text

def supply_details_for_notification(supply):
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
    return text

def new_order_for_supplier(statement, supplier):
    st = statement
    s = supplier
    text = supplier_utils.get_word('new order', chat_id=s.user_id)
    text = text.format(
        id=st.id, applicant=st.user.name, phone=st.user.phone, object=st.object.title
    )
    text += '\n➖➖➖➖➖➖➖\n'
    # orders text
    for order in st.orders.all():
        # dont notify if product is already available on storage
        if order.product_obj:
            continue
        order_text = supplier_utils.get_word('order details', chat_id=s.user_id)
        order_text = order_text.format(
            title = order.product, 
            amount = order.amount,
            product_comment = order.comment
        )
        text += order_text
        text += '\n➖➖➖➖➖➖➖\n'
    return text

def accepted_message_for_supplier(supply):
    st = supply.statement
    supplier = supply.supplier

    order_text = supplier_utils.get_word('order details', chat_id=supplier.user_id)
    products = get_orders_of_statement(st, order_text)

        
    text = '{}\n\n{}\n{}➖ ➖ ➖ ➖ ➖\n\n{}\n\n{}'.format(
        supplier_utils.get_word('your supply is accepted', chat_id=supplier.user_id),
        supplier_utils.get_word('statement details', chat_id=supplier.user_id),
        '{products}',
        supplier_utils.get_word('applicant details', chat_id=supplier.user_id),
        supplier_utils.get_word('supply details', chat_id=supplier.user_id),
        ).replace('\t', '')
    text = text.format(
        order_id=st.pk, products = products,
        applicant=st.user.name, phone=st.user.phone, object=st.object.title,
        supplier=supply.supplier.name, price=supply.price, 
        due=supply.due.strftime('%d.%m.%Y'), comment=supply.comment 
        )

    return text

def statement_status_for_applicant(statement, supply=None):
    user = statement.user
    status = statement.status
    if status == 'conf':
        header_text = applicant_utils.get_word('your statement is confirmed', chat_id=user.user_id)
    elif status == 'cancel':
        header_text = applicant_utils.get_word('your statement is canceled', chat_id=user.user_id)
    elif status == 'end':
        header_text = applicant_utils.get_word('your statement is accepted by supplier', chat_id=user.user_id)
        supply_details_text = applicant_utils.get_word('supply details', chat_id=user.user_id).format(
            supplier=supply.supplier.name, price=supply.price,
            due=supply.due.strftime('%d.%m.%Y'), comment=supply.comment
        )

    order_text = applicant_utils.get_word('order details', chat_id=user.user_id)
    products = get_orders_of_statement(statement, order_text)

    text = '{}\n\n{}\n{}'.format(
        header_text,
        applicant_utils.get_word('statement details', chat_id=user.user_id),
        '{products}'
    )

    text = text.format(
        order_id = statement.pk, products=products,   
    )

    if status == 'end':
        text += '➖ ➖ ➖ ➖ ➖\n\n' + supply_details_text

    return text
import requests
from config import CREATING_STATEMENT_URL as url, ONE_C_SERVER_LOGIN as login, ONE_C_SERVER_PASSWORD as password, DEBUG
from app.models import Statement

result = {
    'supplier': [
        # list suppliers
    ],
    'order': {
        # order details
    }
}

def create_statement_api(statement):
    st = statement
    products = []
    for order in st.orders.all():
        product_id = ''
        warehouse_id = ''
        if order.product_obj:
            product_id = order.product_obj.product_id
            warehouse_id = order.product_obj.warehouse_id
        products.append(
            {
                'product_id': product_id,
                'productTitle': order.product,
                'warehouse_id': warehouse_id,
                'amount': order.amount,
                'comment': order.comment
            }
        )

    statement = {
        'status': 'new',
        'id': st.pk,
        'products': products,
    }
    result['order'] = statement
    try:
        if not DEBUG:
            r = requests.post(url=url, json=result, auth=(login, password))
        # print(r.content.decode())
    except:
        a = 0

def cancel_statement_api(statement):
    st = statement

    order = {
        'status': 'cancel',
        'id': st.pk,
    }
    result['order'] = order
    try:
        if not DEBUG:
            r = requests.post(url=url, json=result, auth=(login, password))
        # print(r.content.decode())
    except:
        a = 0



def add_supply_api(supply):
    st = supply.statement
    result['order'] = {
        'status': 'edit',
        'id': st.pk,
    }

    supplier = {
        'id': supply.supplier.id,
        'supplier': supply.supplier.name,
        'total': supply.price,
        'date': supply.due.strftime('%Y-%m-%d'),
        'comment': supply.comment,
    }
    result['supplier'].append(supplier)

    try:
        if not DEBUG:
            r = requests.post(url=url, json=result, auth=(login, password))
        # print(r.content.decode())
    except:
        a = 0

def confirm_supply_api(supply):
    st = supply.statement
    result['order'] = {
        'status': 'win',
        'id': st.pk,
        'winner': supply.supplier.pk,
    }


    try:
        if not DEBUG:
            r = requests.post(url=url, json=result, auth=(login, password))
        # print(r.content.decode())
    except:
        a = 0

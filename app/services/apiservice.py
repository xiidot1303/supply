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
    order = {
        'status': 'new',
        'id': st.pk,
        'productTitle': st.product,
        'amount': st.amount,
        'comment': st.comment
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
        'productTitle': st.product,
        'amount': st.amount,
        'comment': st.comment
    }

    supplier = {
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

    
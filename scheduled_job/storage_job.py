import json
import requests
from config import STORAGE_URL as url, ONE_C_SERVER_LOGIN as login, ONE_C_SERVER_PASSWORD as password
from app.models import Product

def get_products():
    try:
        response = requests.get(url, auth=(login, password))
        products_list = json.loads(response.content.decode())
        for data in products_list:
            product = data['product']
            warehouse = data['warehouse']
            type = data['type']

            obj = Product.objects.get_or_create(product_id=str(product['id']))[0]
            obj = Product.objects.get(pk=obj.pk)
            obj.title = product['name']
            obj.amount = product['count']
            obj.warehouse = warehouse['name']
            obj.warehouse_id = warehouse['id']
            obj.type = type['name']
            obj.type_id = type['id']

            obj.save()
    except:
        a = 0
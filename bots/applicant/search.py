from django.db.models import Q
from app.models import Statement, Product
from app.services import statementservice
from . import *
from bots import *
from transliterate import translit

def get_string(update, context):
    text = update.inline_query.query
    text_ru = translit(text, 'ru')
    try:
        text_en = translit(text, reversed=True)
    except:
        text_en = text
    text_en = regexing_en(text_en)
    text_ru = regexing_ru(text_ru)
    products = Product.objects.filter(
        Q(title__iregex=text_en) | Q(title__iregex=text_ru) | Q(title__icontains=text)
        )
    type_text = get_word('product type', chat_id=update.inline_query.from_user.id)
    storage_text = get_word('storage', chat_id=update.inline_query.from_user.id)
    description = '{type_text}: {type}\n{storage_text}: {storage}'
    article = [
        inlinequeryresultarticle(
            obj.title, 
            description=description.format(type_text=type_text, storage_text=storage_text, type=obj.type, storage=obj.warehouse),
            product_id=obj.pk
            ) 
            for obj in products
    ]
    if not article:
        article = [
            inlinequeryresultarticle(get_word('not found', chat_id=update.inline_query.from_user.id))
        ]
    
    update_inline_query_answer(update, article)



def regexing_en(text):
    list_couples = [
        'ao', 'xh', 'ie', 'qk', 'cs', 'jy'
    ]

    for i in list_couples:
        text = text.replace(i[0], f'({i[0]}|{i[1]})')
        text = text.replace(i[1], f'({i[0]}|{i[1]})')
        text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

    return text

def regexing_ru(text):
    list_couples = [
        'ао', 'её', 'ыи', 'юу', 'щш'
    ]

    for i in list_couples:
        text = text.replace(i[0], f'({i[0]}|{i[1]})')
        text = text.replace(i[1], f'({i[0]}|{i[1]})')
        text = text.replace(f'{i[0]}|({i[0]}|{i[1]})', f'{i[0]}|{i[1]}')

    return text
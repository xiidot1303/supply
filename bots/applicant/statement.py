from app.models import Statement
from app.services import statementservice, notificationservice, supplierservice, apiservice
from . import *
from bots import *
from bots.applicant.directive import to_the_typing_product_name
from datetime import datetime

def _to_the_typing_product_type(update):
    text = get_word('type product type', update)
    update_message_reply_text(update, text)
    return GET_PRODUCT_TYPE

def _to_the_typing_product_amount(update, order):
    text = get_word('type product amount', update) + ' ({})'.format(order.product)
    update_message_reply_text(update, text)
    return GET_PRODUCT_AMOUNT

def _to_the_typing_product_comment(update, order):
    text = get_word('type product comment', update) + ' ({})'.format(order.product)
    update_message_reply_text(update, text)
    return GET_PRODUCT_COMMENT

def _to_the_asking_action(update, obj):
    text = get_word('your order', update) + ':\n\n'
    orders = statementservice.filter_orders_of_object(obj)
    for order in orders:
        text_order = get_word('order details', update)
        text_order = text_order.format(
            title=order.product, amount=order.amount, product_comment=order.comment
        )
        text_order += '\n➖➖➖➖➖➖➖\n'
        text += text_order
    
    text += '\n' + get_word('end statement or add more', update)
    reply_markup = reply_keyboard_markup(
        [
            [get_word('add product', update)], 
            [get_word('end statement', update)]
        ]
        )

    update_message_reply_text(update, text, reply_markup)
    return GET_ACTION

def _end_statement(update, context, obj):
    
    # send notification to groups
    notificationservice.send_statement_to_groups(obj)
    supplierservice.send_statement_to_suppliers(obj)
    apiservice.create_statement_api(obj)
    
    obj.status = 'wait'
    obj.date = datetime.now()
    obj.save()
    
    text = get_word('completed statement', update).format(id=obj.id)
    update_message_reply_text(update, text)
    main_menu(update, context)
    return ConversationHandler.END

@is_start
def get_product_name(update, context):
    msg = update.message.text
    obj = statementservice.create_and_get_object_by_update(update)
    order = statementservice.get_last_order_of_object(obj)
    if msg == get_word('back', update):
        # check statement has products
        if statementservice.filter_unfinished_objects_by_update(update):
            # delete last order
            statementservice.remove_order_from_obj(obj)
            return _to_the_asking_action(update, obj)

        bot_delete_message(
            update, context, 
            update.message.message_id-1, 
        )

        main_menu(update, context)
        return ConversationHandler.END
    
    order.product = msg
    #check product is available in warehouse
    if '<>?' in msg:
        title, id = msg.split('<>?')
        product_obj = Product.objects.get(pk=int(id))
        order.product_obj = product_obj
        order.product = title 

    order.save()
    bot_delete_message(
        update, context, 
        update.message.message_id-1,
    )

    return _to_the_typing_product_amount(update, order)


@is_start
def get_product_amount(update, context):
    msg = update.message.text
    if msg == get_word('back', update):
        return to_the_typing_product_name(update, context)
    
    obj = statementservice.get_current_object_by_update(update)
    order = statementservice.get_last_order_of_object(obj)
    order.amount = msg
    order.save()

    return _to_the_typing_product_comment(update, order)

@is_start
def get_product_comment(update, context):
    msg = update.message.text
    obj = statementservice.get_current_object_by_update(update)
    order = statementservice.get_last_order_of_object(obj)
    if msg == get_word('back', update):
        return _to_the_typing_product_amount(update, order)
    
    order.comment = msg
    order.save()

    return _to_the_asking_action(update, obj)

@is_start
def get_action(update, context):
    msg = update.message.text
    obj = statementservice.get_current_object_by_update(update)
    order = statementservice.get_last_order_of_object(obj)
    if msg == get_word('add product', update):
        
        # add new order to statement
        statementservice.add_order_to_the_obj(obj)
        return to_the_typing_product_name(update, context)
    elif msg == get_word('end statement', update):
        return _end_statement(update, context, obj)
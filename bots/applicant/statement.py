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

def _to_the_typing_product_amount(update, obj):
    text = get_word('type product amount', update) + ' ({})'.format(obj.product)
    update_message_reply_text(update, text)
    return GET_PRODUCT_AMOUNT

def _to_the_typing_product_comment(update, obj):
    text = get_word('type product comment', update) + ' ({})'.format(obj.product)
    update_message_reply_text(update, text)
    return GET_PRODUCT_COMMENT

def _end_statement(update, context, obj):
    obj.status = 'wait'
    obj.date = datetime.now()
    obj.save()
    
    # send notification to groups
    notificationservice.send_statement_to_groups(obj)
    supplierservice.send_statement_to_suppliers(obj)
    apiservice.create_statement_api(obj)
    
    text = get_word('completed statement', update).format(id=obj.id)
    update_message_reply_text(update, text)
    main_menu(update, context)
    return ConversationHandler.END

@is_start
def get_product_name(update, context):
    msg = update.message.text
    if msg == get_word('back', update):
        bot_delete_message(
            update, context, 
            update.message.message_id-1, 
        )

        main_menu(update, context)
        return ConversationHandler.END
    
    obj = statementservice.create_and_get_object_by_update(update)
    obj.product = msg
    #check product is available in warehouse
    if '<>?' in msg:
        title, id = msg.split('<>?')
        product_obj = Product.objects.get(pk=int(id))
        obj.product_obj = product_obj
        obj.product = title 

    obj.save()
    bot_delete_message(
        update, context, 
        update.message.message_id-1,
    )

    return _to_the_typing_product_amount(update, obj)

@is_start
def get_product_type(update, context): # inactive
    msg = update.message.text
    if msg == get_word('back', update):
        return to_the_typing_product_name(update, context)
    
    obj = statementservice.get_current_object_by_update(update)
    obj.type = msg
    obj.save()

    return _to_the_typing_product_amount(update, obj)
    
@is_start
def get_product_amount(update, context):
    msg = update.message.text
    if msg == get_word('back', update):
        return to_the_typing_product_name(update, context)
    
    obj = statementservice.get_current_object_by_update(update)
    obj.amount = msg
    obj.save()

    return _to_the_typing_product_comment(update, obj)

@is_start
def get_product_comment(update, context):
    msg = update.message.text
    obj = statementservice.get_current_object_by_update(update)
    if msg == get_word('back', update):
        return _to_the_typing_product_amount(update, obj)
    
    obj.comment = msg
    obj.save()

    return _end_statement(update, context, obj)




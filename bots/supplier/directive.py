from bots import *
from . import *
from app.services import (
    supplyservice, 
    statementservice, 
    supplierservice,
    stringservice
    )

def to_the_typing_supply_price(update, context):
    update = update.callback_query
    data = str(update.data)
    if supplyservice.filter_current_objects_by_update(update):
        # update_message_reply_text(update, get_word('', update))
        return 

    if 'supply_statement-' in data:
        *args, id = data.split('-')
        statement = statementservice.get_object_by_id(int(id))
        st = statement
        supplier = supplierservice.get_object_by_update(update)
        if statement.status != 'conf':
            if statement.status == 'cancel':
                bot_answer_callback_query(update, context, get_word('statement is cancelled', update))
            else:
                bot_answer_callback_query(update, context, get_word('statement is already accepted', update))
            text = stringservice.order_info_for_supplier(statement, supplier)
            bot_edit_message_text(update, context, text)
            return
        supplyservice.create_object(statement, supplier)
        text = get_word('type supply price', update) + ' ({} № #n_{})'.format(get_word('order', update), statement.pk)
        button = reply_keyboard_markup(keyboard=[[get_word('main menu', update)]])
        update_message_reply_text(update, text, reply_markup=button)
        bot_answer_callback_query(update, context, get_word('type your own terms', update), show_alert=False)
        return GET_SUPPLY_PRICE

def to_the_active_statements_list(update, context):
    statement_list = statementservice.filter_active_objects()
    supplier = supplierservice.get_object_by_update(update)
    for st in statement_list:
        text = stringservice.order_info_for_supplier(st, supplier)
        i_apply = InlineKeyboardButton(
            text=stringservice.supply(supplier), 
            callback_data='supply_statement-{}'.format(st.pk)
            )
        reply_markup = InlineKeyboardMarkup([[i_apply]])
        bot_send_message(update, context, text, reply_markup)
    
    if not statement_list:
        text = get_word('active orders are not available', update)
        bot_send_message(update, context, text)
    return
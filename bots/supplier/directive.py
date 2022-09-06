from bots import *
from . import *
from app.services import supplyservice, statementservice, supplierservice

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
        if statement.status != 'wait':
            if statement.status == 'cancel':
                bot_answer_callback_query(update, context, get_word('statement is cancelled', update))
            else:
                bot_answer_callback_query(update, context, get_word('statement is already accepted', update))
            text = get_word('new order', update)
            text = text.format(
                id=st.id, applicant=st.user.name, phone=st.user.phone,
            )
            text += '\n➖➖➖➖➖➖➖\n'
            for order in statement.orders.all():
                if order.product_obj:
                    continue
                order_text = get_word('order details', update)
                order_text = order_text.format(
                    title = order.product, 
                    amount = order.amount,
                    product_comment = order.comment
                )
                text += order_text

                text += '\n➖➖➖➖➖➖➖\n'
            bot_edit_message_text(update, context, text)
            return
        supplier = supplierservice.get_object_by_update(update)
        supplyservice.create_object(statement, supplier)
        text = get_word('type supply price', update) + ' ({} № #n_{})'.format(get_word('order', update), statement.pk)
        button = reply_keyboard_markup(keyboard=[[get_word('main menu', update)]])
        update_message_reply_text(update, text, reply_markup=button)
        return GET_SUPPLY_PRICE
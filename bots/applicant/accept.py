from app.services import ( 
    stringservice, 
    supplyservice,
    statementservice,
    )
from bots import *


def accept_supply(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    supply = supplyservice.get_object_by_id(int(id))
    st = supply.statement
    
    text = stringservice.supply_details_for_notification(supply)

    # check, that statement is already ended
    if st.status == 'end':
        bot_answer_callback_query(update, context, 'Это заявление уже принято')
        bot_edit_message_text(update, context, text)
        return

    # change status of supplies
    for obj in supplyservice.filter_supplies_by_statement(st):
        obj.status = 'cancel'
        obj.save()

    try:
        supplyservice.confirm_supply(supply)
        bot_edit_message_text(update, context, text)
        bot_answer_callback_query(update, context, 'Принято! Успешно уведомлен поставщик')
    except:
        bot_answer_callback_query(update, context, 'Ошибка')

def accept_statement(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    statement = statementservice.get_object_by_id(int(id))
    text = stringservice.new_order_for_notification(statement)

    if statementservice.confirm_statement(statement):
        bot_edit_message_text(update, context, text)
        bot_answer_callback_query(update, context, 'Принято! Успешно уведомлен поставщики')
    else:
        bot_edit_message_text(update, context, text)
        bot_answer_callback_query(update, context, 'Это заявление уже одобрено')

def cancel_statement(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    statement = statementservice.get_object_by_id(int(id))
    text = stringservice.new_order_for_notification(statement)

    if statementservice.cancel_statement_by_id(statement.pk):
        bot_edit_message_text(update, context, text)
        bot_answer_callback_query(update, context, 'Успешно отменено')
    else:
        bot_edit_message_text(update, context, text)
        if statement.status == 'cancel':
            bot_answer_callback_query(update, context, 'Уже отменено')
        elif statement.status != 'wait':
            bot_answer_callback_query(update, context, 'Это заявление уже одобрено')


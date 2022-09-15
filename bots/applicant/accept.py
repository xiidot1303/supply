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
        if supply.status == 'cancel':
            bot_edit_message_text(update, context, text+'\n\n❌ <b>Отменено</b>')
        return
    
    bot_edit_message_text(update, context, text+'\n\n⏳ <b>Обработка ...</b>')
    supplyservice.confirm_supply(supply)
    # cancel others supply
    for obj in supplyservice.filter_supplies_by_statement(st).exclude(pk=supply.pk):
        supplyservice.cancel_supply(obj)
    bot_edit_message_text(update, context, text+'\n\n✅ <b>Принято!</b>')
    bot_answer_callback_query(update, context, 'Принято! Успешно уведомлен поставщик')
    
def cancel_supply(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    supply = supplyservice.get_object_by_id(int(id))
    st = supply.statement
    
    text = stringservice.supply_details_for_notification(supply)

    # check, that statement is already ended
    if st.status == 'end':
        bot_answer_callback_query(update, context, 'Это заявление уже принято')
        if supply.status == 'cancel':
            bot_edit_message_text(update, context, text+'\n\n❌ <b>Отменено</b>')
        return
        
    supplyservice.cancel_supply(supply)
    bot_edit_message_text(update, context, text+'\n\n❌ <b>Отменено</b>')
    bot_answer_callback_query(update, context, 'Отменено! Успешно уведомлен поставщик')

def accept_statement(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    statement = statementservice.get_object_by_id(int(id))
    text = stringservice.new_order_for_notification(statement)
    bot_edit_message_text(update, context, text+'\n\n⏳ <b>Обработка ...</b>')
    bot_answer_callback_query(update, context, 'Дождитесь окончания процесса')

    if statementservice.confirm_statement(obj=statement):
        bot_edit_message_text(update, context, text+'\n\n✅ Принято!')
        bot_answer_callback_query(update, context, 'Принято! Успешно уведомлен поставщики')
    else:
        if statement.status == 'cancel':
            bot_answer_callback_query(update, context, 'Это заявление отменено')
            status = '\n\n❌ Отменено'
        else:
            bot_answer_callback_query(update, context, 'Это заявление одобрено')
            status = '\n\n✅ Принято!'
        bot_edit_message_text(update, context, text+status)

def cancel_statement(update, context):
    data = str(update.data)
    *args, id = data.split('-')
    statement = statementservice.get_object_by_id(int(id))
    text = stringservice.new_order_for_notification(statement)

    if statementservice.cancel_statement(obj=statement):
        bot_edit_message_text(update, context, text+'\n\n❌ Отменено')
        bot_answer_callback_query(update, context, 'Успешно отменено')
    else:
        if statement.status == 'cancel':
            bot_answer_callback_query(update, context, 'Уже отменено')
            status = '\n\n❌ Отменено'
        elif statement.status != 'wait':
            bot_answer_callback_query(update, context, 'Это заявление уже одобрено')
            status = '\n\n✅ Принято!'
        bot_edit_message_text(update, context, text+status)


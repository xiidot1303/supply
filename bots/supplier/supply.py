from . import *
from bots import *
from app.services import (
    supplyservice, 
    apiservice, 
    notificationservice,
    stringservice
    )
from datetime import date, datetime

def _to_the_typing_supply_price(update, obj):
    text = get_word('type supply price', update) + ' ({} № #n_{})'.format(get_word('order', update), obj.statement.pk)
    button = reply_keyboard_markup(keyboard=[[get_word('main menu', update)]])
    update_message_reply_text(update, text, button)
    return GET_SUPPLY_PRICE

def _to_the_typing_supply_due(update, obj):
    text = get_word('type supply due', update) + ' ({} № #n_{})'.format(get_word('order', update), obj.statement.pk)
    button = reply_keyboard_markup(keyboard=[[get_word('back', update)]])
    update_message_reply_text(update, text, button)
    return GET_SUPPLY_DUE

def _to_the_typing_supply_comment(update, obj):
    text = get_word('type supply comment', update) + ' ({} № #n_{})'.format(get_word('order', update), obj.statement.pk)
    button = reply_keyboard_markup(keyboard=[[get_word('back', update)]])
    update_message_reply_text(update, text, button)
    return GET_SUPPLY_COMMENT

def _end_supplying(update, context, obj):
    if obj.statement.status == 'end':
        obj.delete()
    else:
        # check supplier already answered to current statement | and delete those
        [obj.delete() for obj in supplyservice.filter_old_supplies_of_current_statement(update, obj)]
        
        obj.date = datetime.now()
        obj.status = 'wait'
        obj.save()
    
        # send notifications
        bot_send_chat_action(update, context)
        apiservice.add_supply_api(obj)
        notificationservice.send_supply_to_groups(obj)
        
    text = stringservice.your_supply_for_supplier(obj)
    update_message_reply_text(update, text)
    main_menu(update, context)
    return ConversationHandler.END

@is_start
def get_supply_price(update, context):
    msg = update.message.text

    obj = supplyservice.get_current_object_by_update(update)
    obj.price = msg
    obj.save()
    bot_delete_message(update, context)
    bot_delete_message(update, context, message_id=update.message.message_id-1)
    return _to_the_typing_supply_due(update, obj)


@is_start
def get_supply_due(update, context):
    msg = update.message.text
    obj = supplyservice.get_current_object_by_update(update)
    if msg == get_word('back', update):
        return _to_the_typing_supply_price(update, obj)
    bot_delete_message(update, context)
    bot_delete_message(update, context, message_id=update.message.message_id-1)
    try:
        day, month, year = msg.split('.')
        year = '20'+year
        due_date = date(day=int(day), month=int(month), year=int(year))
        obj.due = due_date
        obj.save()
        return _to_the_typing_supply_comment(update, obj)

    except:
        update_message_reply_text(update, get_word('incorrect date format', update))
        return


@is_start
def get_supply_comment(update, context):
    msg = update.message.text
    obj = supplyservice.get_current_object_by_update(update)
    if msg == get_word('back', update):
        return _to_the_typing_supply_due(update, obj)

    obj.comment = msg
    obj.save()
    bot_delete_message(update, context)
    bot_delete_message(update, context, message_id=update.message.message_id-1)
    return _end_supplying(update, context, obj)




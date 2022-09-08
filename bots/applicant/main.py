from telegram import ReplyKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle

from app.models import *
from bots.strings import lang_dict
from . import *
from bots import *
import time
from bots.applicant.directive import *
from app.services import (
    notificationservice, 
    supplierservice, 
    supplyservice, 
    stringservice
    )
def start(update, context):
    if is_group(update):
        return 

    if is_registered(update.message.chat.id):
        delete_unfinished_statements(update)
        main_menu(update, context)

    else:
        hello_text = lang_dict['hello']
        update.message.reply_text(
            hello_text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True, one_time_keyboard=True
            ),
        )

        return SELECT_LANG


def settings(update, context):
    make_button_settings(update, context)
    return ALL_SETTINGS


def statement(update, context):
    delete_unfinished_statements(update)
    return to_the_typing_product_name(update, context)

def search(update, context):
    return to_the_searching(update, context)

def accept_supply(update, context):
    update = update.callback_query
    data = str(update.data)

    if not 'accept_supply-' in data:
        return
    
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


def command_supply(update, context):
    if is_group(update):
        notificationservice.create_or_edit_group(update, 'supply')
        update_message_reply_text(update, lang_dict['added group'])
        return 

def command_order(update, context):
    if is_group(update):
        notificationservice.create_or_edit_group(update, 'order')
        update_message_reply_text(update, lang_dict['added group'])
        return 
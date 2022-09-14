from telegram import ReplyKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle

from app.models import *
from bots.strings import lang_dict
from . import *
from bots import *
import time
from bots.applicant.directive import *
from bots.applicant.accept import (
    accept_supply, cancel_supply, 
    accept_statement, cancel_statement
    )
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

def my_statements(update, context):
    return to_the_statements_list(update, context)

def accept(update, context):
    update = update.callback_query
    data = str(update.data)
    bot_send_chat_action(update, context)
    if 'accept_supply-' in data:
        accept_supply(update, context)
    elif 'cancel_supply-' in data:
        cancel_supply(update, context)
    elif 'accept_statement-' in data:
        accept_statement(update, context)
    elif 'cancel_statement-' in data:
        cancel_statement(update, context)


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
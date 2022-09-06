from bots import *
from . import *
from app.services import statementservice

def to_the_typing_product_name(update, context):
    text = get_word('type product name', update)
    # send message with keyboard buttons
    buttons = reply_keyboard_markup(keyboard=[[get_word('back', update)]])
    message = bot_send_message(update, context, text, buttons)
    # bot_delete_message(update, context, message)

    # send search message with inline buttons
    text = get_word('click search button', update)
    i_search = InlineKeyboardButton(text=get_word('search', update), switch_inline_query_current_chat='')
    reply_markup = InlineKeyboardMarkup([[i_search]])
    update_message_reply_text(update, text, reply_markup)
    return GET_PRODUCT_NAME

def to_the_searching(update, context):
    
    text = get_word('click search button', update)
    # i_back = InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu')
    i_search = InlineKeyboardButton(text=get_word('search', update), switch_inline_query_current_chat='')
    reply_markup = InlineKeyboardMarkup([[i_search]])
    # message = bot_send_message(update, context, text, reply_keyboard_remove())
    # bot_delete_message(update, context, message.message_id)
    update_message_reply_text(update, text, reply_markup=reply_markup)
    # return SEARCHING
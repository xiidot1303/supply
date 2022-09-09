from bots import *
from . import *
from app.services import statementservice, stringservice, supplyservice

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

def to_the_statements_list(update, context):
    statements = statementservice.filter_active_statements_by_update(update)
    update_message_reply_text(
        update, 
        get_word('your statements', update), 
        reply_keyboard_markup([[get_word('main menu', update)]])
        )
    for st in statements:
        supply = None
        markup = None
        if st.status == 'end':
            supply = supplyservice.get_confirmed_supply_of_statement(st)
            i_got = InlineKeyboardButton(text=get_word('got', update), callback_data='supplied_statement-{}'.format(st.pk))
            markup = InlineKeyboardMarkup([[i_got]])
        text = stringservice.statement_info_for_applicant(st, supply)
        bot_send_message(update, context, text, markup)

    return CLICK_STATEMENT
from bots.strings import lang_dict
from . import *
from bots.supplier.directive import to_the_typing_supply_price


def start(update, context):
    if is_registered(update.message.chat.id):
        delete_unfinished_supplies(update)
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

@is_start
def settings(update, context):
    make_button_settings(update, context)
    return ALL_SETTINGS

@is_start
def supply(update, context):
    return to_the_typing_supply_price(update, context)    

def fallback(update, context):
    update = update.callback_query
    text = get_word('go to main menu', update)
    bot_answer_callback_query(update, context, text, show_alert=False)
    return
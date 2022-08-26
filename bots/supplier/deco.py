from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from bots.supplier.conversationList import *
from bots.supplier.utils import *
from bots.strings import lang_dict

def is_start_registr(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except:
            update = args[0].callback_query
            data = update.data
        id = update.message.chat.id
        if update.message.text == "/start":
            update.message.reply_text(
                lang_dict['hello'],
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True
                ),
            )
            return SELECT_LANG

        else:
            return func(*args, **kwargs)

    return func_arguments


def is_start(func):  # This deco break registration if user send /start.
    def func_arguments(*args, **kwargs):
        context = args[1]
        bot = context.bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except Exception:
            try:
                update = args[0].callback_query
                data = update.data
            except:
                return func(*args, **kwargs)
                
        id = update.message.chat.id
        user = get_user_by_update(update)
        if (
            update.message.text == "/start"
            or data == "main_menu"
            or update.message.text == get_word("main menu", update)
        ):

            delete_unfinished_supplies(update)
            main_menu(args[0], args[1])
            return ConversationHandler.END
        elif not user.access:
            update.message.reply_text(get_word('no access', update))
            return 
        else:
            return func(*args, **kwargs)

    return func_arguments

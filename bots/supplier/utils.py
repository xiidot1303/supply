from bots.strings import lang_dict
from app.models import Supplier, Supply
from app.services import supplyservice
from bots.supplier.conversationList import *
from bots import *

def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing

    bot = context.bot
    keyboard = [
        [get_word('settings', update)],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    bot.send_message(
        update.message.chat.id,
        get_word("main menu", update),
        reply_markup=reply_markup,
    )
    check_username(update)


def make_button_settings(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing
    bot = context.bot
    keyboard = [
        [get_word("change lang", update)],
        [get_word("change name", update)],
        [get_word("change phone number", update)],
        [get_word("main menu", update)],
    ]
    bot.send_message(
        update.message.chat.id,
        get_word("settings desc", update),
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True),
    )




def is_registered(id):
    if Supplier.objects.filter(user_id=id).exclude(phone=None):
        return True
    else:
        return False


def get_word(text, update=None, chat_id=None):
    if not chat_id:
        chat_id = update.message.chat.id

    user = Supplier.objects.get(user_id=chat_id)
    if user.lang == "uz":
        return lang_dict[text][0]
    else:
        return lang_dict[text][1]


def get_user_by_update(update):
    user = Supplier.objects.get(user_id=update.message.chat.id)
    return user

def check_username(update):
    user = get_user_by_update(update)

    if user.username != update.message.chat.username:
        user.username = update.message.chat.username
        user.save()
    if user.firstname != update.message.chat.first_name:
        user.firstname = update.message.chat.first_name
        user.save()

def delete_unfinished_supplies(update):
    [obj.delete() for obj in supplyservice.filter_current_objects_by_update(update)]
from bots import *
from bots.strings import lang_dict
from app.models import *
from app.services import statementservice
from bots.applicant.conversationList import *


def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing

    bot = context.bot
    keyboard = [
        [get_word('start statement', update)],
        [get_word('my statements', update)],
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

def get_objects_reply_markup():
    keyboard = [[obj.title] for obj in Object.objects.all()]
    markup = reply_keyboard_markup(keyboard)
    return markup


def is_registered(id):
    if Applicant.objects.filter(user_id=id).exclude(phone=None):
        return True
    else:
        return False

def is_group(update):
    if update.message.chat.type == 'group' or update.message.chat.type == 'supergroup':
        return True
    return False

def get_word(text, update=None, chat_id=None):
    if not chat_id:
        chat_id = update.message.chat.id

    user = Applicant.objects.get(user_id=chat_id)
    if user.lang == "uz":
        return lang_dict[text][0]
    else:
        return lang_dict[text][1]


def get_user_by_update(update):
    user = Applicant.objects.get(user_id=update.message.chat.id)
    return user

def check_username(update):
    user = get_user_by_update(update)

    if user.username != update.message.chat.username:
        user.username = update.message.chat.username
        user.save()
    if user.firstname != update.message.chat.first_name:
        user.firstname = update.message.chat.first_name
        user.save()

def delete_unfinished_statements(update):
    for obj in statementservice.filter_unfinished_objects_by_update(update):
        # delete orders
        for order in obj.orders.all():
            order.delete()
        # delete photos
        for photo in obj.photos.all():
            photo.delete()
        obj.delete() 

def save_and_get_photo(update, context):
    bot = context.bot
    photo_id = bot.getFile(update.message.photo[-1].file_id)
    *args, file_name = str(photo_id.file_path).split('/')
    d_photo = photo_id.download('files/photos/{}'.format(file_name))
    return str(d_photo).replace('files/', '')
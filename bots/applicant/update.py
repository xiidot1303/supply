import asyncio
from telegram import Bot, InputTextMessageContent
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence, BasePersistence
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    InlineQueryHandler
)

from config import APPLICANT_BOT_API_TOKEN, DEBUG

from bots.strings import lang_dict
from bots.applicant.conversationList import *
from bots.applicant import (
    main, login, settings, statement, search
)

persistence = PicklePersistence(filename="persistencebot")

bot_obj = Bot(APPLICANT_BOT_API_TOKEN)

if not DEBUG:  # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=10, use_context=True, persistence=persistence)

else:  # in development
    updater = Updater(
        token=APPLICANT_BOT_API_TOKEN, workers=10, use_context=True, persistence=persistence,
    )
    dp = updater.dispatcher

login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        SELECT_LANG: [MessageHandler(Filters.text(lang_dict["uz_ru"]), login.select_lang)],
        GET_NAME: [MessageHandler(Filters.text, login.get_name)],
        GET_CONTACT: [MessageHandler(Filters.all, login.get_contact)],
    },
    fallbacks=[],
    name="login",
    persistent=True,

)

settings_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict["settings"]), main.settings)],
    states={
        ALL_SETTINGS: [MessageHandler(Filters.text, settings.all_settings)],
        LANG_SETTINGS: [
            CallbackQueryHandler(settings.lang_settings),
            CommandHandler("start", settings.lang_settings),
        ],
        PHONE_SETTINGS: [MessageHandler(Filters.all, settings.phone_settings)],
        NAME_SETTINGS: [MessageHandler(Filters.text, settings.name_settings)],
    },
    fallbacks=[],
    name="settings",
    persistent=True,
  
)


statement_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict['start statement']), main.statement)],
    states={
        GET_PRODUCT_NAME: [MessageHandler(Filters.text, statement.get_product_name)],
        GET_PRODUCT_AMOUNT: [MessageHandler(Filters.text, statement.get_product_amount)],
        GET_PRODUCT_COMMENT: [MessageHandler(Filters.text, statement.get_product_comment)],
        GET_ACTION: [MessageHandler(Filters.text, statement.get_action)],
        GET_OBJECT: [MessageHandler(Filters.text, statement.get_object)],
        FINISH_STATEMENT: [MessageHandler(Filters.text, statement.finish_statement)],
    },
    fallbacks=[],
    name='statement',

    persistent=True
)

search_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict['search']), main.search)],
    states={
        SEARCHING: [
            CommandHandler('start', search.get_string),
            CallbackQueryHandler(search.get_string)
        ],
    },
    fallbacks=[],
    name='search',
    persistent=True,
)

search_handler = MessageHandler(Filters.text(lang_dict['search']), main.search)

dp.add_handler(CommandHandler('order', main.command_order))
dp.add_handler(CommandHandler('supply', main.command_supply))
dp.add_handler(InlineQueryHandler(search.get_string)),
dp.add_handler(search_handler)
dp.add_handler(statement_handler)
dp.add_handler(settings_handler)
dp.add_handler(login_handler)
dp.add_handler(CallbackQueryHandler(main.accept_supply))


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

from config import SUPPLIER_BOT_API_TOKEN, DEBUG

from bots.strings import lang_dict
from bots.supplier.conversationList import *
from bots.supplier import (
    main, login, settings, supply
)

persistence = PicklePersistence(filename="persistencebot2")

bot_obj = Bot(SUPPLIER_BOT_API_TOKEN)

if not DEBUG:  # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=10, use_context=True, persistence=persistence)
else:  # in development
    updater = Updater(
        token=SUPPLIER_BOT_API_TOKEN, workers=10, use_context=True, persistence=persistence
    )
    dp = updater.dispatcher


#### HANDLERS ####

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

supply_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(main.supply)],
    states={
        GET_SUPPLY_PRICE: [MessageHandler(Filters.text, supply.get_supply_price)],
        GET_SUPPLY_DUE: [MessageHandler(Filters.text, supply.get_supply_due)],
        GET_SUPPLY_COMMENT: [MessageHandler(Filters.text, supply.get_supply_comment)],
    },
    fallbacks=[],
    name='supply',
    persistent=True
)

dp.add_handler(supply_handler)
dp.add_handler(settings_handler)
dp.add_handler(login_handler)

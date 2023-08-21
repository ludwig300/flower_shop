import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("День рождения", callback_data='birthday'),
         InlineKeyboardButton("Свадьба", callback_data='wedding')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('К какому событию готовимся? Выберите один из вариантов, либо выберите свой.', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'birthday':
        # Здесь можно добавить логику для дня рождения
        query.edit_message_text(text="Выбран день рождения!")
    elif query.data == 'wedding':
        # Здесь можно добавить логику для свадьбы
        query.edit_message_text(text="Выбрана свадьба!")


def main():
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

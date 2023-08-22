import os

import django
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Updater, MessageHandler, Filters)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_shop.settings")
django.setup()

from django.conf import settings

from flowershop_bot.models import Bouquet, Order


GET_NAME, GET_PHONE = range(2)


def ask_customer_info(update, context, event_type, budget):
    context.user_data['event_type'] = event_type
    context.user_data['budget'] = budget
    update.callback_query.message.reply_text(text="Пожалуйста, введите ваше имя:")
    return GET_NAME


def get_name(update, context):
    print("get_name called")
    name = update.message.text
    context.user_data['name'] = name
    update.message.reply_text("Пожалуйста, введите ваш номер телефона:")
    return GET_PHONE


def get_phone(update, context):
    phone = update.message.text
    context.user_data['phone'] = phone

    selected_bouquet = context.user_data['bouquet']

    order = Order(
        customer_name=context.user_data['name'],
        customer_phone=phone,
        bouquet=selected_bouquet
    )
    order.save()

    update.message.reply_text("Спасибо за ваш заказ! В скором времени мы с вами свяжемся.")
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Заказ отменен. Если у вас возникнут вопросы, пожалуйста, свяжитесь с нами.')
    context.user_data.clear()
    return ConversationHandler.END


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

    if query.data.startswith('order'):
        _, event_type, budget = query.data.split('_')
        return ask_customer_info(update, context, event_type, budget)
    elif query.data in ['birthday', 'wedding']:
        ask_budget(update, context, query.data)
    elif query.data.endswith('_500') or query.data.endswith('_1000') or query.data.endswith('_5000') or query.data.endswith('_no-matter'):
        event_type, budget = query.data.split('_')[:2]
        display_bouquet(update, context, event_type, budget)


def ask_budget(update, context, event_type):
    keyboard = [
        [InlineKeyboardButton("500", callback_data=f'{event_type}_500')],
        [InlineKeyboardButton("1000", callback_data=f'{event_type}_1000')],
        [InlineKeyboardButton("5000", callback_data=f'{event_type}_5000')],
        [InlineKeyboardButton("Не важно", callback_data=f'{event_type}_no-matter')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(text="На какую сумму рассчитываете?", reply_markup=reply_markup)


def get_bouquet(event_type, budget):
    if budget == '500':
        bouquets = Bouquet.objects.filter(price__lte=500)
    elif budget == '1000':
        bouquets = Bouquet.objects.filter(price__gte=500, price__lte=1000)
    elif budget == '5000':
        bouquets = Bouquet.objects.filter(price__gte=1000, price__lte=5000)
    elif budget == 'no-matter':
        bouquets = Bouquet.objects.all()
    else:
        bouquets = Bouquet.objects.none()

    print(f"event_type: {event_type}, budget: {budget}, bouquets: {bouquets}")

    bouquet = bouquets.first() if bouquets else None

    if bouquet:
        return {
            'name': bouquet.name,
            'image_url': bouquet.image.url,
            'description': bouquet.description,
            'price': bouquet.price
        }
    else:
        return None


def display_bouquet(update, context, event_type, budget):
    bouquet = get_bouquet(event_type, budget)
    if bouquet is not None:
        context.user_data['bouquet'] = Bouquet.objects.get(name=bouquet['name'])

        text = f"Букет: {bouquet['name']}\nОписание: {bouquet['description']}\nСтоимость: {bouquet['price']}"
        keyboard = [
            [InlineKeyboardButton("Заказать этот букет", callback_data=f'order_{event_type}_{budget}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        image_path = os.path.join(settings.MEDIA_ROOT, bouquet['image_url'].lstrip('/media/'))

        with open(image_path, 'rb') as image_file:
            update.callback_query.message.reply_photo(
                photo=image_file,
                caption=text,
                reply_markup=reply_markup
            )
    else:
        text = "К сожалению, подходящих букетов не найдено."
        update.callback_query.message.reply_text(text)


def main():
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            GET_NAME: [MessageHandler(
                Filters.text & ~Filters.command,
                get_name
            )],
            GET_PHONE: [MessageHandler(
                Filters.text & ~Filters.command,
                get_phone
            )]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

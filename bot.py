# from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

from gpt import ChatGptService
# from util import (load_message, load_prompt, send_text, send_image, send_text_buttons, show_main_menu,
#                   default_callback_handler)
from util import *
import credentials
import random


# 1.1 Ф-ція стартового меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓'
        # Додати команду в меню можна так:
        # 'command': 'button text'
    })

# 1.3 Ф-ція random для пошуку випадкових фактів
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1.4 Завантаження фото з файлу images
    await send_image(update, context, 'random')
    # 1.5 Завантажує prompt (вхідні дані пошуку)
    prompt = load_prompt("random")
    # print(prompt)
    # 1.6 відправляємо в чат gpt prompt (вхідні дані пошуку) та текст
    response = await chat_gpt.send_question(prompt, 'Давай рандомний факт')
    # 1.7 отриману відповідь віддаємо користувачеві
    await send_text(update, context, response)
    # 1.8 Створюємо кнопки вибору продовжити чи закінчити
    await send_text_buttons(update, context, response, {"random_closed": "Закінчити", "random_next": "Хочу ще факт!"})

# 1.10 Ф-ція random_button_next для закінчення чи продовження випадкових фактів
async def random_button_next(update: Update, context):
    # 1.11 Збереження повернутого значення обраної кнопки "random_closed" чи "random_next"
    query = update.callback_query.data
    # print(query)
    if query == "random_closed":
        # 1.11.1 При даному виборі виклик ф-ції start, (повернення) на стартову сторінку
        await start(update, context)
    elif query == "random_next":
        # 1.11.2 При даному виборі виклик ф-ції random, продовження пошуку цікавих фактів
        await random(update, context)
    # 1.12 вимкнення режиму очікування кнопки (переливання)
    await update.callback_query.answer()

# 1.14 Ф-ція gpt для активації посилання на чат gpt
async def gpt(update, context):
    await send_image(update, context, "gpt")
    gpt_text_load = load_message("gpt")
    # print(gpt_text_load)
    await send_text(update, context, gpt_text_load)

# 1.16 Ф-ція gpt_dialog для написання, відправки питання, та отримання відповіді з чат gpt
async def gpt_dialog(update, context):
    # 1.17 збереження тексту питання
    question_text = update.message.text
    # print(text)
    # 1.18 Завантажує prompt (вхідні дані пошуку)
    prompt = load_prompt("gpt")
    # 1.19 відправляємо в чат gpt prompt (вхідні дані пошуку), текст та отримання відповіді
    answer = await chat_gpt.send_question(prompt, question_text)
    # print(answer)
    await send_text(update, context, answer)

# 1.20 Ф-ція talk для діалогу з відомою особистістю
async def talk(update, context):
    await send_image(update, context, "talk")
    talk_text_load = load_message("talk")
    # print(talk_text_load)
    await send_text(update, context, talk_text_load)



chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
# 1.2 Запускаємо обране посилання "start" та ф-ції start
app.add_handler(CommandHandler("start", start))
# 1.9 Запускаємо обране посилання "random" та ф-ції random
app.add_handler(CommandHandler("random", random))
# 1.15 Запускаємо обране посилання "gpt" та ф-ції gpt
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_dialog))
app.add_handler(CommandHandler("talk", talk))


# Зареєструвати обробник колбеку можна так:
# 1.13 Запускаємо обрану кнопку зі всіма значеннями починаючи з "random_"
app.add_handler(CallbackQueryHandler(random_button_next, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()

# from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

from gpt import ChatGptService
# from util import (load_message, load_prompt, send_text, send_image, send_text_buttons, show_main_menu,
#                   default_callback_handler)
from util import *
import credentials
import random


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

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, 'random')
    prompt = load_prompt("random")
    # print(prompt)
    # відправляємо в чат gpt набіл запитів з ramdom
    response = await chat_gpt.send_question(prompt, 'Давай рандомний факт')
    # отриману відповідь віддаємо користувачеві
    await send_text(update, context, response)
    await send_text_buttons(update, context, response, {"random_closed": "Закінчити", "random_next": "Хочу ще факт!"})

async def random_button_next(update: Update, context):
    query = update.callback_query.data
    if query == "random_closed":
        await start(update, context)
    elif query == "random_next":
        await random(update, context)
    await update.callback_query.answer()

async def gpt(update, context):
    await send_image(update, context, "gpt")
    gpt_text_load = load_message("gpt")
    # print(gpt_text_load)
    await send_text(update, context, gpt_text_load)

async def gpt_dialog(update, context):
    text = update.message.text
    # print(text)
    prompt = load_prompt("gpt")
    answer = await chat_gpt.send_question(prompt, text)
    # print(answer)
    await send_text(update, context, answer)


chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_dialog))


# Зареєструвати обробник колбеку можна так:
app.add_handler(CallbackQueryHandler(random_button_next, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()

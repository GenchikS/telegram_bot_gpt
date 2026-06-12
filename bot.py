# from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

from gpt import ChatGptService
# from util import (load_message, load_prompt, send_text, send_image, send_text_buttons, show_main_menu,
#                   default_callback_handler)
# Використання всіх ф-цій з файлу util
from util import *
import credentials
import random

##########
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

##########
# 1.3 Ф-ція random для пошуку випадкових фактів
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1.3.2 Присвоєння режиму використання значення random
    dialog.mode = "random"
    # print(dialog.mode)
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

##########
# 1.14 Ф-ція gpt для активації посилання на чат gpt
async def gpt(update, context):
    dialog.mode = "gpt"
    # print(dialog.mode)
    await send_image(update, context, "gpt")
    gpt_text_load = load_message("gpt")
    # print(gpt_text_load)
    await send_text(update, context, gpt_text_load)

# 1.16 Ф-ція gpt_dialog для написання, відправки питання, та отримання відповіді з чат gpt
async def gpt_dialog(update, context):
    # 1.17 збереження тексту питання
    question_text = update.message.text
    # print(question_text)
    # 1.18 Завантажує prompt (вхідні дані пошуку)
    prompt = load_prompt("gpt")
    # 1.19 відправляємо в чат gpt prompt (вхідні дані пошуку), текст та отримання відповіді
    answer = await chat_gpt.send_question(prompt, question_text)
    # print(answer)
    await send_text(update, context, answer)

##########
# 1.21 Ф-ція talk для діалогу з відомою особистістю
async def talk(update, context):
    dialog.mode = "talk"
    await send_image(update, context, "talk")
    talk_text_load = load_message("talk")
    # print(talk_text_load)
    await send_text(update, context, talk_text_load)
    await send_text_buttons(update, context, talk_text_load,{
        "talk_cobain": "Курт Кобейн",
        "talk_queen": "Єлизавета II",
        "talk_tolkien": "Джон Толкін",
        "talk_nietzsche": "Фрідріх Ніцше",
        "talk_hawking": "Стівен Гокінг",
        })

# 1.22 Ф-ція talk_button для обрання відомої особи для діалогу
async def talk_button(update: Update, context):
    query = update.callback_query.data
    # 1.23 Збереження обраного персонажу
    dialog.name = query
    await update.callback_query.answer()
    # print(query)
    await send_image(update, context, query)
    talk_text = load_message("talk_message")
    await send_text(update, context, talk_text)
    dialog.mode = "message"


# 1.24 Ф-ція talk_dialog для повідомлень діалогу
async def talk_dialog(update: Update, context):
    # 1.25 Збереження введеного питання
    question_text = update.message.text
    # print(dialog.name)
    # print(context)
    # 1.26 Діставання збереженого персонажу та отримання промту на нього
    prompt = load_prompt(dialog.name)
    # 1.27 Відправка промту та питання
    answer = await chat_gpt.send_question(prompt, question_text)
    await send_text_buttons(update, context, answer, {"answer_exit": "Закінчити діалог"})

# 1.28 Ф-ція talk_dialog_exit закінчити діалог
async def talk_dialog_button_exit(update: Update, context):
    # 1.29 Отримання натискання кнопки Закінчити діалог
    query = update.callback_query.data
    if query == "answer_exit":
        dialog.name = None
        await start(update, context)

##########
# 1.31 Створення ф-ції quiz, аналогічно як і talk
async def quiz(update: Update, context):
    dialog.mode = "quiz"
    await send_image(update, context, "quiz")
    # await send_text(update, context, load_message("quiz"))
    await send_text_buttons(update, context, load_message("quiz"), {
        "quiz_prog": "програмування python",
        "quiz_math": "математика",
        "quiz_biology": "біологія",
    })

async def quiz_button_dialog(update: Update, context):
    await update.callback_query.answer()
    query = update.callback_query.data
    # print(query)
    quiz.list = query
    prompt = load_prompt("quiz")
    # print(prompt)
    question_gpt = await chat_gpt.send_question(prompt, quiz.list)
    # print(question_gpt)
    quiz.questions = await send_text(update, context, question_gpt)

async def quiz_dialog(update: Update, context):
    # dialog.mode = "quiz"
    user_answer = update.message.text
    # print(user_answer)
    prompt = load_prompt("quiz_question")
    answer = f'{quiz.questions} + {user_answer}'
    answer_gpt = await chat_gpt.send_question(prompt, answer)
    # print(answer)

    await send_text_buttons(update, context, answer_gpt, {
        "quiz_more": "продовжуємо тему далі",
        "quiz_next": "змінити тему",
        "quiz_exit": "закінчити quiz"
    })



##########
# 1.3.3 Створення ф-ції перевірки режиму та запуску відповідної ф-ції
async def status(update: Update, context):
    if dialog.mode == "random":
        await random_button_next(update, context)
    elif dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "talk":
        await talk_button(update, context)
    elif dialog.mode == "message":
        await talk_dialog(update, context)
    elif dialog.mode == "quiz":
        await quiz_dialog(update, context)



# 1.3.1 Використання ф-ції Dialog для створення режиму використання
dialog = Dialog()
dialog.mode = None

dialog.name = None
quiz.questions = None

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
# 1.2 Запускаємо обране посилання "start" та ф-ції start
app.add_handler(CommandHandler("start", start))
# 1.9 Запускаємо обране посилання "random" та ф-ції random
app.add_handler(CommandHandler("random", random))
# 1.15 Запускаємо обране посилання "gpt" та ф-ції gpt
app.add_handler(CommandHandler("gpt", gpt))
# 1.20 Запускаємо ф-цію gpt_dialog, обробник діалогу
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, status))
app.add_handler(CommandHandler("talk", talk))
app.add_handler(CommandHandler("quiz", quiz))

# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk_dialog))


# Зареєструвати обробник колбеку можна так:
# 1.13 Запускаємо обрану кнопку зі всіма значеннями починаючи з "random_"
app.add_handler(CallbackQueryHandler(random_button_next, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(talk_button, pattern='^talk.*'))
# 1.30 Створення обробника talk_dialog_button_exit для кнопки зі значенням answer
app.add_handler(CallbackQueryHandler(talk_dialog_button_exit, pattern='^answer.*'))
app.add_handler(CallbackQueryHandler(quiz_button_dialog, pattern='^quiz.*'))

# app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

CHANNEL_USERNAME = "s1ivkers"
FAKE_USER_COUNT = 13000

async def is_subscribed(application, user_id):
    try:
        member = await application.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    app = context.application

    if not await is_subscribed(app, user_id):
        keyboard = [
            [InlineKeyboardButton("👉 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ Я подписался", callback_data='check_sub')]
        ]
        await update.message.reply_text(
            f"🌀 Добро пожаловать в GX Haven!\n\n"
            f"🔒 Для доступа подпишись на канал:\n"
            f"👉 https://t.me/{CHANNEL_USERNAME}\n\n"
            f"✅ После подписки — жми на кнопку \"Я подписался\"",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await send_menu(update, context)

async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1. Ответчик-сладенький", callback_data='mode_1')],
        [InlineKeyboardButton("2. Какой ты…", callback_data='mode_2')],
        [InlineKeyboardButton("3. Шизопредсказатель", callback_data='mode_3')],
        [InlineKeyboardButton("4. Скинь прикол", callback_data='mode_4')],
        [InlineKeyboardButton("5. Смешные новости", callback_data='mode_5')],
        [InlineKeyboardButton(f"🔥 У бота уже {FAKE_USER_COUNT} пользователей! 🔥", callback_data='fake_count')]
    ]

    text = "Выбери режим:\n\n"
    text += "1️⃣ Ответчик-сладенький\n"
    text += "2️⃣ Какой ты…\n"
    text += "3️⃣ Шизопредсказатель\n"
    text += "4️⃣ Скинь прикол\n"
    text += "5️⃣ Смешные новости\n"

    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    app = context.application

    if query.data == 'check_sub':
        if await is_subscribed(app, user_id):
            await query.answer("Подписка подтверждена! 🎉")
            await send_menu(update, context)
        else:
            await query.answer("Ты всё ещё не подписан. Подпишись, чтобы продолжить.", show_alert=True)
    elif query.data == 'mode_1':
        await query.answer()
        await query.edit_message_text(
            "💬 Спроси что-нибудь, я отвечу в стиле канала. Например:\n"
            "— 'Сколько сейчас времени?'\n"
            "— 'Время вспомнить, как ты обещал сесть на диету в марте. Уже июнь, сладенький.'\n\n"
            "Попробуй команду /obidetemya чтобы получить рофельные оскорбления."
        )
    elif query.data == 'mode_2':
        await query.answer()
        await query.edit_message_text(
            "🎲 /kto_ya — Узнай, какой ты трэш-герой!\n"
            "Пример:\n"
            "\"Ты — жирный файтер с душой девственника, играешь в CS с вайфай-мышкой и мечтаешь о бате, который вернётся с молоком.\""
        )
    elif query.data == 'mode_3':
        await query.answer()
        await query.edit_message_text(
            "🔮 Шизопредсказатель шлёт тебе послание:\n"
            "\"Сегодня ты снова не напишешь ей, зато узнаешь, как на вкус холодная гречка в 3 ночи.\"\n"
            "\"Будущее туманно, но точно пахнет дошиком.\""
        )
    elif query.data == 'mode_4':
        await query.answer()
        await query.edit_message_text(
            "😂 Мем-дайджест активирован! Отправь команду /daj, чтобы получить мем с твоими подписями."
        )
    elif query.data == 'mode_5':
        keyboard = [
            [InlineKeyboardButton("Перейти к смешным новостям в канале", url=f"https://t.me/{CHANNEL_USERNAME}")]
        ]
        await query.answer()
        await query.edit_message_text(
            "🤣 Чтобы посмеяться, заходи в наш канал с новостями и мемами!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == 'fake_count':
        await query.answer(f"У бота уже {FAKE_USER_COUNT} пользователей! Не будь последним 😉", show_alert=True)
    else:
        await query.answer()

async def obidetemya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    insults = [
        "Ты — ходячий баг в системе жизни, сладенький.",
        "Обидеть тебя? Легко! Ты — синий экран моего настроения.",
        "Ты как Wi-Fi без пароля — вроде бы доступен, а толку нет."
    ]
    insult = random.choice(insults)
    await update.message.reply_text(insult)

async def kto_ya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    combos = [
        "Ты — жирный файтер с душой девственника, играешь в CS с вайфай-мышкой и мечтаешь о бате, который вернётся с молоком.",
        "Ты — сладкий вампир на пенсии. Твоя суперсила — удаляться из всех чатов перед контрольной.",
        "Ты — забытый герой скиллов, но зато умеешь в CTRL+C и CTRL+V."
    ]
    combo = random.choice(combos)
    await update.message.reply_text(combo)

async def daj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    memes = [
        "Когда ты забыл сделать домашку, но бот всегда на страже 😂",
        "Я хотел быть умным, но решил стать мемом.",
        "Понедельник начинается в воскресенье, а я всё ещё не выспался."
    ]
    meme = random.choice(memes)
    keyboard = [[InlineKeyboardButton("Ещё один", callback_data='mode_4')]]
    await update.message.reply_text(meme, reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    TOKEN = "7588969393:AAH0xuauIHrkzu9Fuiq1EO8MCEwL2skEnEc"
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("obidetemya", obidetemya))
    application.add_handler(CommandHandler("kto_ya", kto_ya))
    application.add_handler(CommandHandler("daj", daj))

    application.run_polling()

if __name__ == '__main__':
    main()

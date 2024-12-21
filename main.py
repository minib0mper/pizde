import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7639229274:AAEqPbPGCqF9JXxx4gkMeEcbVl78BGthLPw"
num = 0

ban_words = [
    # Русский мат
    "блять", "блядь", "пизда", "пиздец", "хуй", "хуйня", "хуеплет", "хуесос", "ебать", 
    "ебало", "ебаный", "ебануть", "ебучий", "нахуй", "сука", "гандон", "гондон", "долбоеб", 
    "мудак", "ублюдок", "мразь", "гнида", "говно", "ссанина", "сосать", "давалка", "падла", 
    "шлюха", "проститутка", "чмо", "тварь", "курва", "пидор", "пидорас", "педик", "гей", 
    "член", "залупа", "гавнюк", "козел", "паскуда", "скотина", "хуила", "сволочь", "тупица", 
    "имбецил", "кретин", "урод", "гадина", "выкидыш", "чучело", "мразота", "паскуда", "мудила", 
    "ублюдина", "сучара", "гнида", "шлюшка", "проститка", "дурак", "кретинка", "дегенерат", 
    "обезьяна", "скотина", "маразматик", "маразм", "гондончик", "туфта", "шмара", "отброс",

    # Английский мат
    "fuck", "shit", "bitch", "asshole", "bastard", "crap", "dick", "faggot", "cunt", 
    "piss", "whore", "slut", "damn", "motherfucker", "suck", "prick", "cock", "twat", "jerk", 
    "loser", "fucker", "scumbag", "retard", "moron", "idiot", "numbnuts", "douche", "douchebag", 
    "fucktard", "wanker", "tosser", "bollocks", "arsehole", "shithead", "craphole", "butthole", 
    "screw you", "eat shit", "get fucked", "bullshit", "damn you", "you bastard",

    # Расистские и дискриминационные выражения
    "нацист", "фашист", "расист", "гитлер", "негр", "жид", "мразота", "цыган", "хохол", 
    "чурка", "москаль", "ватник", "пиндос", "узкоглазый", "нигер", "chink", "nigger", "nigga", 
    "gypsy", "retard", "homo", "tranny", "spic", "wetback", "sandnigger",

    # Дополнительные уничижительные выражения
    "тупой", "долбанутый", "недоумок", "идиотина", "лох", "оболтус", "осёл", "дура", 
    "дурень", "жопа", "жопошник", "придурок", "дебилоид", "бездарь", "неудачник", "ничтожество", 
    "отстой", "ничтожный", "ничтожество", "безмозглый", "бездарный", "выкидыш", "дно", 
    "хлам", "шлак", "днище", "недоносок", "жалкий", "глупец", "жлоб", "мазила", "поц", 
    "прохиндей", "свинья", "кретин", "скотина",

    # Фразы с нецензурной лексикой (русский)
    "иди нахуй", "пошел на хуй", "соси хуй", "хуй с ним", "да пошел ты", "иди в жопу", 
    "на хрен", "ебаный в рот", "еб твою мать", "ебанутый", "херня", "хрен с тобой", "гори в аду",

    # Фразы с нецензурной лексикой (английский)
    "fuck off", "go to hell", "suck my dick", "son of a bitch", "piece of shit", "eat shit",
    "get fucked", "shut the fuck up", "you’re an idiot", "you’re a loser", "screw you", 
    "go die", "rot in hell", "goddamn",

    # Устаревшие оскорбления (русский)
    "жиробас", "жирдяй", "растяпа", "болван", "дурак", "обезьяна", "хамло", "уродина", 
    "шут гороховый", "дуралей", "балбес", "кретин", "недоумок",

    # Устаревшие оскорбления (английский)
    "scoundrel", "knave", "cur", "wretch", "simpleton", "dunce", "clod", "lout", 
    "nincompoop", "blockhead", "imbecile"
]

async def rec(query):
    if num == 10:
        query.message.reply_text(f"Оставьте заявку на вступление для поддержки разработчика\n https://t.me/+_PslAnpWv5owY2Uy")
        num = 0
    else:
        num += 1

# Логирование визитов пользователей
def log_visit(user_id, username):
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{visit_time} - User ID: {user_id}, Username: {username}\n"
    try:
        with open("data1.txt", "r", encoding='utf-8') as f:
            if f"User ID: {user_id}" in f.read():
                return  # Уже записано
    except FileNotFoundError:
        pass
    # Запись нового визита
    with open("data1.txt", "a", encoding='utf-8') as f:
        f.write(log_entry)

# Проверка сообщения на запрещённые слова
async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()  # Приведение текста к нижнему регистру
    user_id = update.effective_user.id  # ID пользователя
    username = update.effective_user.username or "не указано"
    message_id = update.message.message_id  # ID сообщения
    
    # Проверка на запрещённые слова
    if any(word in message for word in ban_words):
        log_visit(user_id, username)
        await update.message.reply_text(f"{username} использовал запрещённое слово. Ему выдан мут на 10 минут.")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
        until_time = update.message.date + timedelta(minutes=10)
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_time
        )

# Главный старт бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "не указано"
    log_visit(user_id, username)
    await update.message.reply_text("Привет! Я модераторский бот. Следите за словами.")
    await menu(update)

# Кнопки для меню
async def menu(update: Update):
    keyboard = [
        [InlineKeyboardButton("Запустить бота!", callback_data="starter")],
        [InlineKeyboardButton("О боте", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

# Обработка нажатия кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "starter":
        await query.message.reply_text("Бот уже активен и читает сообщения!")
    elif query.data == "info":
        await query.message.reply_text("Я модераторский бот. Удаляю запрещённые слова и выдаю мут нарушителям.")

# Команда для показа списка пользователей
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('data1.txt', 'r', encoding='utf-8') as f:
            users = f.readlines()
            count = len(users)
            await update.message.reply_text(f"Количество зарегистрированных пользователей: {count}")
    except FileNotFoundError:
        await update.message.reply_text("Логи пользователей отсутствуют.")

# Основная функция запуска бота
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("users", users))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    print("Бот запущен!")
    main()

import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7463462122:AAEJFKA-ICGqGtTaW366-vcIyv6e094wYAk"  # Замените на ваш токен
Money = 0
money = 0
lang = 0
async def langu(user_id, update):
    """ Функция для отправки сообщения в зависимости от данных в файле. """
    with open('data.txt', 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        id_found = False
        for line in lines:
            if line.startswith(str(user_id)):
                parts = line.split()
                if len(parts) >= 2:
                    number = parts[1]
                    id_found = True
                    await menuu(update)
                    break
        if not id_found:
            # Если ID не найден, отправляем сообщение
            await update.message.reply_text("Ваш ID не найден в базе данных.")

async def data(user_id, money):
    """Обновляет или добавляет данные в файл data.txt."""
    try:
        # Лог для отладки
        print(f"Обновляем данные: user_id={user_id}, money={money}")

        # Проверяем существование файла и логируем путь к нему
        file_path = 'data.txt'
        print(f"Путь к файлу: {os.path.abspath(file_path)}")

        # Считываем существующие строки из файла (если файл существует)
        lines = []
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Файл data.txt не найден, он будет создан.")

        # Проверяем, есть ли уже запись для данного user_id
        id_found = False
        for i in range(len(lines)):
            if lines[i].startswith(str(user_id)):
                # Обновляем запись
                lines[i] = f"{user_id} {money}\n"
                id_found = True
                break

        # Если запись не найдена, добавляем новую
        if not id_found:
            lines.append(f"{user_id} {money}\n")

        # Перезаписываем файл с обновлёнными данными
        with open(file_path, 'w', encoding='ISO-8859-1') as file:
            file.writelines(lines)

        # Лог для отладки
        print("Данные успешно записаны в файл.")

    except Exception as e:
        # Логирование ошибок
        print(f"Ошибка при работе с файлом: {e}")



def log_visit(user_id, username):
    """ Логирование визитов пользователей. """
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{visit_time} - User ID: {user_id}, Username: {username}"

    try:
        with open("loxi.txt", "r", encoding='ISO-8859-1') as f:
            for line in f:
                if f"User ID: {user_id}" in line:
                    return  # Логирование уже существует, ничего не делаем
    except FileNotFoundError:
        pass

    # Запись нового визита
    with open("loxi.txt", "a", encoding='ISO-8859-1') as f:
        f.write(log_entry + "\n")

async def menuu(update):
    await update.message.reply_text(
        f"👋 Привет, друг!\n\n"
        f"Хочешь легко зарабатывать деньги? Этот бот поможет тебе заработать, выполняя простые задания. 💰\n\n"
        f"Как начать зарабатывать прямо в Telegram:\n"
        f"🔹 **Выполняй задания** и получай деньги сразу.\n"
        f"🔹 **Приглашай друзей** по своей реферальной ссылке и зарабатывай **$1** за каждого друга, который нажмёт 'start'. 💵\n"
        f"🔹 **Выводи заработанные деньги** каждый день. 🔥\n\n"
        f"🤔 *Почему мы это делаем?*\n"
        f"Популярные Telegram-каналы платят нам за привлечение подписчиков, а мы делимся прибылью с тобой. Это выгодно всем!📈📈\n\n"
        f"Начни прямо сейчас и смотри, как растёт твой доход! 🚀")
    await menu(update)

async def menu(query):
    keyboard = [
        [InlineKeyboardButton("Зарабатывать!🔥", callback_data="earn")],
        [InlineKeyboardButton("Баланс💰", callback_data="balic")],
        [InlineKeyboardButton("Пригласить друга👥", callback_data="lox")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Выбери вариант!📋", reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    money = 0
    global lang, Money
    user_id = update.effective_user.id
    username = update.effective_user.username or "не указано"
    log_visit(user_id, username)
    await data(user_id, money)
    await langu(user_id, update)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    global Money, money
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await menu(query)
    elif query.data == "earn":
        await data(user_id, money)
        if money == 0:
            link = 'https://t.me/+_PslAnpWv5owY2Uy'
            money += 1
            Money = '1$'
            await data(user_id, money)
        elif money == 1:
            link = 'https://t.me/+PT9OOK_m7FI1YWQy'
            money += 1
            Money = '2$'
            await data(user_id, money)
        elif money == 2:
            link = 'https://t.me/+hOfy2MT0X8JjNzE6'
            money += 1
            Money = '3$'
            await data(user_id, money)
        elif money == 3:
            link = 'Ссылки кончились, простите'
            await query.message.reply_text(f"{link}")
            money = 0
        keyboard = [
            [InlineKeyboardButton(f"Подписаться✅", callback_data=f"{link}")],
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Подпишись для вознаграждения!📈📈", reply_markup=reply_markup)
    elif query.data == "balic":
        data(user_id, money)
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton(f"Вывести деньги💳", callback_data="loxx")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Ваш баланс: "f"{Money}", reply_markup=reply_markup)
    elif query.data == "loxx":
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton(f"Пригласить друга👬", callback_data="lox")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Для вывода требуется пригласить 10 друзей по ссылке:", reply_markup=reply_markup)
    elif query.data == "lox":
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton("Скопировать ссылку", url=f"@EZPAY9_bot")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)   
        await query.message.reply_text(f"Скопируйте ссылку и отправьте другу\n @EZPAY9_bot", reply_markup=reply_markup)

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('loxi.txt', 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()
            line_count = len(lines)

        await update.message.reply_text(f"Количество пользователей: {line_count}")
    except FileNotFoundError:
        await update.message.reply_text("Логи отсутствуют.")

def main():
    global money
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == "__main__":
    main()

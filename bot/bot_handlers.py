from utils.json_utils import read_json, write_json
from config.config import TELEGRAM_TOKEN
from utils.weather import fetch_weather
from utils.logger import log_message
from telebot import types
import telebot


# Создаём объект бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# parse_mode="HTML" - все сообщения поддерживают HTML-разметку


@bot.message_handler(commands=['start'])
def start(message):
    """
    Обрабатывает команду /start — приветствует пользователя.
    """
    log_message(message)  # Логируем команду
    # Имя пользователя: сначала username, иначе first_name
    username = message.from_user.username or message.from_user.first_name

    # Отправляем приветственное сообщение
    bot.send_message(
        message.chat.id,
        f"👋 Привет <b>@{username}!</b>\n"
        "Напиши название города:"
    )

@bot.message_handler(commands=['setcity'])
def setcity(message):
    """
    Обрабатывает команду /setcity — запоминает город для рассылки.
    """
    log_message(message)  # Логируем команду
    # Отправляем сообщение с кнопкой "🛑 Остановить"
    bot.send_message(
        message.chat.id,
        "🏙 Введите название города:",
        reply_markup=stop_city_keyboard()  # Прикрепляем клавиатуру
        )
    # Регистрируем обработчик следующего сообщения от этого пользователя
    bot.register_next_step_handler(message, save_city)

def save_city(message):
    """
    Сохраняет введённый пользователем город в JSON по chat_id.
    """
    log_message(message)  # Логируем ввод города
    chat_id = str(message.chat.id)  # Преобразуем chat_id в строку для ключа JSON
    city = message.text.strip().title()  # Убираем пробелы и делаем первую букву города заглавной

    # Проверка города через API
    data = fetch_weather(city)  # Получаем погоду (если город существует)
    if not data or data.get("cod") != 200:  # Если ошибка или код != 200 (город не существует)
        # Отправляем сообщение с кнопкой "🛑 Остановить"
        sent = bot.send_message(
            message.chat.id,
            "❌ Город не найден. Попробуйте снова:",
            reply_markup=stop_city_keyboard()  # Прикрепляем клавиатуру
        )

        # Регистрируем ожидание следующего ввода города на отправленном сообщении
        bot.register_next_step_handler(sent, save_city)
        return  # Выходим, чтобы не продолжать сохранение

    # Если город существует: Читаем существующие данные
    data = read_json("user_cities.json") or {}

    # Записываем / Обновляем город
    data[chat_id] = city
    write_json("user_cities.json", data)

    # Подтверждаем сохранение
    bot.send_message(
        message.chat.id,
        f"✅ Город <b>{city.title()}</b> сохранён!"
    )

def stop_city_keyboard():
    """
    Создаёт Inline-клавиатуру с кнопкой "Остановить".
    """
    # Создаём Inline-клавиатуру с кнопкой "Остановить"
    kb = types.InlineKeyboardMarkup()

    # Добавляем кнопку "🛑 Остановить" в клавиатуру
    kb.add(types.InlineKeyboardButton("🛑 Остановить", callback_data="stop_city_input"))
    # callback_data → значение, которое придёт в callback_query_handler при нажатии

    # Возвращаем готовую клавиатуру, чтобы можно было прикрепить её к сообщению
    return kb

# Декоратор ловит callback-запросы (не текстовые сообщения)
# func=... фильтрует только те колбэки, у которых callback_data == "stop_city_input"
@bot.callback_query_handler(func=lambda c: c.data == "stop_city_input")
def stop_city_input(c):  # Параметр c — это объект telebot.types.CallbackQuery
    """
    Обрабатывает нажатие на кнопку "Остановить" при вводе города.
    """
    bot.answer_callback_query(c.id)  # Закрываем индикатор загрузки кнопки ("Часики")

    # Снимаем зарегистрированный step_handler для этого чата
    # Если пользователь отправит текст после нажатия «Остановить», save_city не сработает
    bot.clear_step_handler_by_chat_id(c.message.chat.id)

    # Пытаемся изменить сообщение с кнопкой на текст "Отменено"
    try:
        bot.edit_message_text(
            "🚫 Ввод города отменён.",
            c.message.chat.id,
            c.message.message_id
        )
    except Exception:
        # Если редактирование не удалось (например, по времени) — просто отправим новое
        bot.send_message(c.message.chat.id, "🚫 Ввод города отменён.")

@bot.message_handler(commands=['mycity'])
def mycity(message):
    """
    Обрабатывает команду /mycity — Выводит сохранённый город пользователя.
    """
    log_message(message)  # Логируем команду

    # Загружаем словарь с городами пользователей из файла
    # Если файл пустой или не найден, получаем пустой словарь {}
    data = read_json("user_cities.json") or {}

    # Получаем город по chat.id пользователя
    city = data.get(str(message.chat.id))

    if city:
        # Если город найден — отправляем его пользователю
        bot.send_message(
            message.chat.id,
            f"🏙 Ваш сохранённый город: <b>{city}</b>"
        )
    else:
        # Если город не найден — просим сохранить его через /setcity
        bot.send_message(
            message.chat.id,
            "⚠ У вас ещё не сохранён город.\nИспользуйте /setcity для сохранения."
        )

@bot.message_handler(content_types=['text'])
def send_weather(message):
    """
    Обрабатывает текстовые сообщения — принимает название города,
    получает информацию о погоде и отправляет её пользователю.
    """
    log_message(message)  # Логируем каждое текстовое сообщение
    
    # Извлекаем название города из текста и убираем пробелы по краям
    city = message.text.strip()
    
    # Получаем "сырой" JSON с данными о погоде от API
    data = fetch_weather(city)

    # Если данных нет или API вернул ошибку - выводим сообщение об ошибке
    if not data or data.get("cod") != 200:
        bot.reply_to(message, "❌ Город указан неверно или сервер недоступен!")
        return

    # Обрабатываем данные о погоде в удобный для нас формат
    weather = get_weather(data)

    # Формируем и отправляем сообщение с результатом
    bot.reply_to(message, format_weather_message(city, weather))

def get_weather(weather):
    """
    Принимает "сырой" JSON с погодой от API и возвращает словарь
    с уже готовыми данными для вывода пользователю.
    """
    temp = weather['main']['temp']  # Температура
    weather_main = weather['weather'][0]['main']  # Основное состояние погоды (Rain, Clear и т.д.)
    weather_description = weather['weather'][0]['description']  # Описание погоды на русском (например, "пасмурно")
    humidity = weather['main']['humidity']  # Влажность воздуха (%)
    wind_speed = weather['wind']['speed']  # Скорость ветра (м/с)

    return {
        "temp": temp,                      # Температура
        "weather_main": weather_main,      # Основное состояние (Rain, Snow, Clear...)
        "weather_description": weather_description,  # Описание погоды
        "humidity": humidity,              # Влажность (%)
        "wind_speed": wind_speed           # Скорость ветра (м/с)
    }

def format_weather_message(city: str, weather: dict) -> str:
    """
    Формирует текстовое сообщение о погоде с эмодзи.
    """
    # Сопоставление типов погоды с эмодзи
    emoji_map = {
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Atmosphere": "🌫️",
        "Clear": "☀️",
        "Clouds": "☁️"
    }

    emoji = emoji_map.get(weather["weather_main"], "🌍")  # Эмодзи по умолчанию — планета
    
    return (
        f"В городе <b>{city}</b> {weather['weather_description']}, {weather['temp']}°C {emoji}\n"
        f"💧 Влажность: {weather['humidity']}%, 💨 Ветер: {weather['wind_speed']} м/с"
    )

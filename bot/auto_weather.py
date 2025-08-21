from bot.bot_handlers import bot, format_weather_message, get_weather
from apscheduler.schedulers.background import BackgroundScheduler
from utils.weather import fetch_weather
from utils.json_utils import read_json
from datetime import datetime
from zoneinfo import ZoneInfo


# Часовой пояс Казахстана
KZ_TZ = ZoneInfo("Asia/Almaty")

# Планировщик
scheduler = BackgroundScheduler(timezone=KZ_TZ)


def send_weather_auto():
    """
    Отправляет сохранённым пользователям погоду в определённые часы.
    """
    now = datetime.now(KZ_TZ)  # Получаем текущее время по КЗ
    print(f"[AUTO WEATHER] Запуск задачи — {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Список часов, в которые бот будет отправлять погоду
    allowed_hours = {7, 10, 13, 16, 19, 22}

    # Загружаем сохранённых пользователей и их города
    users = read_json("user_cities.json") or {}

    for chat_id, city in users.items():
        data = fetch_weather(city)  # Запрашиваем погоду для города

        # Если API вернул ошибку — сообщаем пользователю
        if not data or data.get("cod") != 200:
            bot.send_message(chat_id, f"❌ Не удалось получить погоду для {city}")
            continue

        # Получаем готовую структуру с погодой
        weather = get_weather(data)
        
        # Форматируем и отправляем сообщение пользователю
        bot.send_message(chat_id, format_weather_message(city, weather), parse_mode="html")


def start_auto_weather():
    """
    Запускает APScheduler с задачами на каждые 3 часа (с 07:00 до 22:00).
    """
    # Часы, в которые будет отправляться погода
    allowed_hours = [7, 10, 13, 16, 19, 22]

    # Создаём задачи для каждого часа
    for hour in allowed_hours:
        scheduler.add_job(
            send_weather_auto,
            trigger="cron",
            hour=hour,
            minute=0,
            id=f"weather_{hour}",
            replace_existing=True
        )

    scheduler.start()
    print("[AUTO WEATHER] Планировщик запущен")

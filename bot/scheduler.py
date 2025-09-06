from utils.weather import fetch_weather, is_valid_weather_response
from apscheduler.schedulers.background import BackgroundScheduler
from bot.dependencies import user_cities_json
from abc import ABC, abstractmethod
from bot.bot_handlers import bot
from datetime import datetime
from zoneinfo import ZoneInfo


# Часовой пояс Казахстана
KZ_TZ = ZoneInfo("Asia/Almaty")


class Observer(ABC):
    """
    Базовый интерфейс наблюдателя.
    """
    @abstractmethod
    def update(self, chat_id: int, city: str, weather_data: dict):
        pass


class WeatherBotNotifier(Observer):
    """
    Наблюдатель: отвечает за отправку погоды пользователям через Telegram-бота.
    """
    def update(self, chat_id: int, city: str, weather_data: dict):
        # Если API вернул ошибку — сообщаем пользователю
        if not is_valid_weather_response(weather_data):  # Если ответ неверный (город не найден, ошибка сервера)
            bot.send_message(chat_id, f"❌ Не удалось получить погоду для {city}")
            return

        from handlers.weather import get_weather, format_weather_message
        weather_obj = get_weather(weather_data)  # Получаем готовую структуру с погодой

        # Готовим сообщение и отправляем его пользователю
        message = format_weather_message(city, weather_obj)
        bot.send_message(chat_id, message)


class LoggerObserver(Observer):
    """
    Наблюдатель: просто логирует факт рассылки погоды.
    (Может использоваться для отладки или админ-уведомлений.)
    """
    def update(self, chat_id: int, city: str, weather_data: dict):
        now = datetime.now(KZ_TZ)
        print(f"[LOG] {now.strftime('%Y-%m-%d %H:%M:%S')} | Chat: {chat_id}, City: {city}")


class WeatherSubject:
    """
    Издатель (Subject):
    - хранит список наблюдателей (подписчиков)
    - уведомляет их при каждом обновлении данных
    """
    def __init__(self):
        self._observers: list[Observer] = []  # Список подписчиков

    def subscribe(self, observer: Observer):
        """Подписать нового наблюдателя"""
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        """Отписать наблюдателя"""
        self._observers.remove(observer)

    def notify(self, chat_id: int, city: str, data: dict):
        """Рассылает обновление всем подписчикам"""
        for observer in self._observers:
            observer.update(chat_id, city, data)


# Планировщик
scheduler = BackgroundScheduler(timezone=KZ_TZ)

subject = WeatherSubject()  # Создаём Subject (издатель)
subject.subscribe(WeatherBotNotifier())  # Подписчик: Бот
subject.subscribe(LoggerObserver())  # Подписчик: Логгер


def send_weather_auto():
    """
    Получает погоду и оповещает наблюдателей.
    """
    now = datetime.now(KZ_TZ)  # Получаем текущее время по КЗ
    print(f"[AUTO WEATHER] Запуск задачи — {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Загружаем сохранённых пользователей и их города
    users = user_cities_json.read_json() or {}

    for chat_id, city in users.items():
        data = fetch_weather(city)  # Запрашиваем погоду для города
        subject.notify(chat_id, city, data)


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

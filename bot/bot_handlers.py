from bot.handlers.start import register_start_handler
from bot.handlers.city import register_city_handlers
from bot.handlers.weather import register_weather_handler
from bot.middlewares import setup_middlewares
from config.config import TELEGRAM_TOKEN
import telebot


# Создаём объект бота
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML", use_class_middlewares=True)
# parse_mode="HTML" - все сообщения поддерживают HTML-разметку

# Подключаем middleware
setup_middlewares(bot)

# Подключаем обработчики
register_start_handler(bot)
register_city_handlers(bot)
register_weather_handler(bot)

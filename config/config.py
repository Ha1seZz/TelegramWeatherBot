from dotenv import load_dotenv
import os


# Загружаем переменные окружения
load_dotenv()

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Получаем API-ключ для сервиса OpenWeather
API_KEY = os.getenv("WEATHER_API")

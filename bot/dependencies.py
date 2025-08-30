from utils.json_utils import JsonUtils
from utils.logger import Logger

# Создаём объект для работы с json
user_cities_json = JsonUtils("TelegramWeatherBot/logs/user_cities.json")

# Создаём объект для работы с логами
logs = Logger()

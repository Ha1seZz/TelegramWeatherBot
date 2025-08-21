from config.config import API_KEY
import requests


def fetch_weather(city: str) -> dict | None:
    """
    Получает погоду по названию города с сервиса OpenWeather.

    Аргументы:
        city (str): Название города.

    Возвращает:
        dict | None: Данные о погоде в формате JSON или None, если запрос не удался.
    """
    try:
        # URL API для получения текущей погоды
        url = f"https://api.openweathermap.org/data/2.5/weather"

        # Параметры запроса
        params = {
            "q": city,          # Название города
            "appid": API_KEY,   # API-ключ
            "units": "metric",  # Градусы в Цельсиях
            "lang": "ru"        # Описание погоды на русском
        }

        # Отправка GET-запроса
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Если статус-код не 200 — вызовет исключение
        return response.json()  # Возвращаем данные в формате Python-словаря

    # Любая ошибка сети или сервера - возвращаем None
    except requests.RequestException:
        return None

from utils.weather import fetch_weather, is_valid_weather_response


def register_weather_handler(bot):
    @bot.message_handler(content_types=['text'])
    def send_weather(message):
        """
        Обрабатывает текстовые сообщения — принимает название города,
        получает информацию о погоде и отправляет её пользователю.
        """   
        # Извлекаем название города из текста и убираем пробелы по краям
        city = message.text.strip()
    
        # Получаем "сырой" JSON с данными о погоде от API
        data = fetch_weather(city)

        # Если данных нет или API вернул ошибку - выводим сообщение об ошибке
        if not is_valid_weather_response(data):  # Если ответ неверный (город не найден, ошибка сервера)
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

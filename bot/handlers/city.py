from utils.weather import fetch_weather, is_valid_weather_response
from bot.dependencies import user_cities_json
from bot.keyboards import stop_city_keyboard


def register_city_handlers(bot):
    @bot.message_handler(commands=['setcity'])
    def setcity(message):
        """
        Обрабатывает команду /setcity — запоминает город для рассылки.
        """
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
        chat_id = str(message.chat.id)  # Преобразуем chat_id в строку для ключа JSON
        city = message.text.strip().title()  # Убираем пробелы и делаем первую букву города заглавной

        # Проверка города через API
        data = fetch_weather(city)  # Получаем погоду (если город существует)
        if not is_valid_weather_response(data):  # Если ответ неверный (город не найден, ошибка сервера)
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
        data = user_cities_json.read_json() or {}

        # Записываем / Обновляем город
        data[chat_id] = city
        user_cities_json.write_json(data)

        # Подтверждаем сохранение
        bot.send_message(
            message.chat.id,
            f"✅ Город <b>{city.title()}</b> сохранён!"
        )

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
        # Загружаем словарь с городами пользователей из файла
        # Если файл пустой или не найден, получаем пустой словарь {}
        data = user_cities_json.read_json() or {}

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

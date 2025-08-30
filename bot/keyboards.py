from telebot import types


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

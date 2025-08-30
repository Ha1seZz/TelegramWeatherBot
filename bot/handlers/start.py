def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        username = message.from_user.username or message.from_user.first_name
        bot.send_message(
            message.chat.id,
            f"👋 Привет <b>@{username}!</b>\nНапиши название города:"
        )

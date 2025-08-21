from auto_weather import start_auto_weather
from bot_handlers import bot


if __name__ == "__main__":
    # Запускаем автоматическую рассылку погоды
    start_auto_weather()

    # Запускаем бота (блокирующий вызов)
    print("🤖 Бот запущен...")
    # skip_pending=True - чтобы бот не обрабатывал старые апдейты
    bot.infinity_polling(skip_pending=True)

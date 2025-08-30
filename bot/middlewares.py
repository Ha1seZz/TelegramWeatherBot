from bot.dependencies import logs
from telebot import TeleBot


class LoggingMiddleware:
    update_types = ['message']

    def __init__(self, logger):
        self.logger = logger

    def pre_process(self, message, data):
        """Выполняется ДО вызова хэндлера"""
        self.logger.log_message(message)

    def post_process(self, message, data, exception):
        """После хэндлера (можно пропустить)"""
        pass


def setup_middlewares(bot: TeleBot):
    bot.setup_middleware(LoggingMiddleware(logs))

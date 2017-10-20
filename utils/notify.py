try:
    from _config import telegram_info
except ImportError:
    from config_template import telegram_info


class TelegramBot:
    def __init__(self):
        from telegram import Bot
        self.bot = Bot(token=telegram_info.token)

    def send_message(self, message):
        self.bot.send_message(chat_id=telegram_info.bot_chat_id, text=message)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from logger import _Logger
from Extensions.BeepBoop import BeepBoop
from Extensions.TutorialMethods import TutorialMethods
from Extensions.TherapyAssistant import TherapyAssistant

logger = _Logger.get_instance().logger


class MedBot(Updater):

    def __init__(self, bot_token: str):
        Updater.__init__(self, token=bot_token, use_context=True)
        self.extensions = []
        logger.info("MedBot Initialized")

    def add_extension(self, cls):
        extension = cls(self)
        for func in extension.get_supported_class_methods():
            prefix, func_name = func.__name__.split("_", 1)
            if prefix == "ch":
                self.dispatcher.add_handler(CommandHandler(func_name, func), extension.group)
            elif prefix == "mh":
                self.dispatcher.add_handler(MessageHandler(Filters.text, func), extension.group)
            elif prefix == "chj":
                self.dispatcher.add_handler(CommandHandler(func_name, func, pass_job_queue=True), extension.group)

        self.extensions.append(extension)
        command_list = [func.callback.__name__ for func in self.dispatcher.handlers[extension.group]]
        log_info = [f"extension {cls.__name__} with following commands added:"]
        log_info += ['    '+func_name for func_name in command_list]
        logger.info("\n".join(log_info))

    def run(self):
        self.start_polling()
        logger.info("Bot is running")
        self.idle()


if __name__ == "__main__":
    """"Test if bot initialization and adding of extension works correctly"""
    bot = MedBot("2044001529:AAEKz1we54SABO2umcz6cfjnnZ2K2oiKEA8")
    bot.add_extension(TutorialMethods)
    logger.info(f"\n{bot.dispatcher.handlers}")
    bot.add_extension(TherapyAssistant)
    logger.info(f"\n{bot.dispatcher.handlers}")

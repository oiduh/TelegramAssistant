from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from Tools.Logger import Logger
from Extensions import TutorialMethods, BeepBoop
from Extensions.ExtensionManager import ExtensionManager
from CommandManager.CommandManager import CommandType

logger = Logger.get_instance().logger


class MedBot(Updater):

    def __init__(self, bot_token: str):
        self.extension_manager = ExtensionManager()
        Updater.__init__(self, token=bot_token, use_context=True)
        logger.info("MedBot Initialized")

    def add_extension(self, module):
        _group, _commands = self.extension_manager.add_commands(module)

        for command in _commands:
            _name = command.__name__
            _type = command.__command_type__
            if _type == CommandType.COMMAND_HANDLER:
                self.dispatcher.add_handler(CommandHandler(_name, command), _group)
            elif _type == CommandType.MESSAGE_HANDLER:
                self.dispatcher.add_handler(MessageHandler(Filters.text, command), _group)
            elif _type == CommandType.COMMAND_HANDLER_JOB:
                self.dispatcher.add_handler(CommandHandler(_name, command, pass_job_queue=True), _group)
            elif _type == CommandType.CALLBACK_QUERY_HANDLER:
                self.dispatcher.add_handler(CallbackQueryHandler(command), _group)

        command_list = [(func.callback.__name__, func.callback.__command_type__.name) for
                        func in self.dispatcher.handlers[_group]]
        log_info = [f"extension {module.__name__} with following commands added:"]
        log_info += ['    ' + cmd_name + (10-len(cmd_name))*' ' + cmd_type for cmd_name, cmd_type  in command_list]
        logger.info("\n".join(log_info))
        cmd_test = command_list[-1]
        print(cmd_test)


    def run(self):
        self.start_polling()
        logger.info("Bot is running")
        self.idle()


if __name__ == "__main__":
    """"Test if bot initialization and adding of extension works correctly"""
    bot = MedBot("2044001529:AAEKz1we54SABO2umcz6cfjnnZ2K2oiKEA8")
    bot.add_extension(TutorialMethods)
    logger.info(f"\n{bot.dispatcher.handlers}")
    bot.add_extension(BeepBoop)
    logger.info(f"\n{bot.dispatcher.handlers}")

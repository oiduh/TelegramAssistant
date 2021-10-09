from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from Tools.Logger import Logger
from Extensions import TutorialMethods, BeepBoop, TherapyAssistant
from Extensions.ExtensionManager import ExtensionManager
from CommandManager.CommandManager import CommandType, COMMAND_TYPE_ATTR, ALIASES_ATTR
from types import ModuleType

logger = Logger.get_instance().logger


class MedBot(Updater):

    def __init__(self, bot_token: str):
        self.extension_manager = ExtensionManager()
        Updater.__init__(self, token=bot_token, use_context=True)
        logger.info("MedBot Initialized")

    def add_extension(self, module: ModuleType) -> None:
        _group, _commands = self.extension_manager.add_commands(module)

        # TODO: check for commands with common aliases -> warn user
        def flatten(_list):
            return [item for sublist in _list for item in sublist]
        print("-"*80)
        cmds = flatten(self.dispatcher.handlers.values())
        print(dir(cmds[0]) if len(cmds) > 0 else None)
        print([x.callback.__command_type__ for x in cmds])
        print([x.callback.__aliases__ for x in cmds if ALIASES_ATTR in dir(x)])
        print([x.command for x in cmds if x.callback.__command_type__ == CommandType.COMMAND_HANDLER])
        print("-"*80)

        for command in _commands:
            _cmd_list = {command.__name__}
            if hasattr(command, COMMAND_TYPE_ATTR):
                _type = getattr(command, COMMAND_TYPE_ATTR)
            else:
                raise Exception("not a command, is this possible?")
            if hasattr(command, ALIASES_ATTR):
                _aliases = set(getattr(command, ALIASES_ATTR))
                if _aliases:
                    _cmd_list = _cmd_list.union(_aliases)
            if _type == CommandType.COMMAND_HANDLER:
                self.dispatcher.add_handler(CommandHandler(_cmd_list, command), _group)
            elif _type == CommandType.MESSAGE_HANDLER:
                self.dispatcher.add_handler(MessageHandler(Filters.text, command), _group)
            elif _type == CommandType.COMMAND_HANDLER_JOB:
                self.dispatcher.add_handler(CommandHandler(_cmd_list, command, pass_job_queue=True), _group)
            elif _type == CommandType.CALLBACK_QUERY_HANDLER:
                self.dispatcher.add_handler(CallbackQueryHandler(command), _group)

        print("-"*80)
        cmds = flatten(self.dispatcher.handlers.values())
        print(dir(cmds[0]) if len(cmds) > 0 else None)
        print([x.callback.__aliases__ for x in cmds if ALIASES_ATTR in dir(x)])
        print("-"*80)


        # TODO: rework the logger messages for this method
        command_list = \
            [
                (
                    func.callback.__name__,
                    func.callback.__command_type__.name,
                    func.command if func.callback.__command_type__ == CommandType.COMMAND_HANDLER else []
                ) for func in self.dispatcher.handlers[_group]
            ]
        log_info = [f"extension {module.__name__} with following commands added:"]
        log_info += ['    ' + cmd_name + (20 - len(cmd_name)) * ' ' + cmd_type + (30 - len(cmd_type)) * ' ' + '(aliases: ' + ', '.join(cmd_aliases) + ')' for cmd_name, cmd_type, cmd_aliases in command_list]
        logger.info("\n".join(log_info))

    def run(self) -> None:
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
    #bot.add_extension(TherapyAssistant)
    #logger.info(f"\n{bot.dispatcher.handlers}")

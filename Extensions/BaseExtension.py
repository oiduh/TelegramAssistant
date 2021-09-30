from logger import _Logger
import inspect

logger = _Logger.get_instance().logger

VALID_COMMAND_PREFIXES = ["ch", "mh", "chj", "cqh"]

"""
    TODO: add more handlers if necessary

function prefixes for distinction:
    ch -> CommandHandler
    mh -> MessageHandler
    chj -> CommandHandler/Job
    cqh -> CallbackQueryHandler
    n -> non-supported/helper function
"""


class BaseExtension:
    # basically a counter for Extensions
    init_group = 0

    def __init__(self, bot):
        self.bot = bot
        cmds = [func_cls for _, func_cls in inspect.getmembers(self.__class__, inspect.isfunction)]
        self.commands = [func for func in cmds if func.__name__.split("_")[0] in VALID_COMMAND_PREFIXES]
        logger.info(f"{self.__class__.__name__} initialized")
        self.group = BaseExtension.init_group
        BaseExtension.init_group += 1

    def get_supported_class_methods(self):
        return self.commands

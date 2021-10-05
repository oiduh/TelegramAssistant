from enum import Enum, auto


class CommandType(Enum):
    COMMAND_HANDLER = auto()
    MESSAGE_HANDLER = auto()
    COMMAND_HANDLER_JOB = auto()
    CALLBACK_QUERY_HANDLER = auto()
